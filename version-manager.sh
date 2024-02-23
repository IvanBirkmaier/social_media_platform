#!/usr/bin/env bash

#####################################
### Utility functions declaration ###
#####################################

# Extracts major, minor and patch number as well as suffix of a given version string
extract_version_components() {
    local version=$1
    IFS='.-+' read -r major minor patch suffix <<< "$version"
    echo "$major $minor $patch $suffix"
}

# Function to compare two semantic versions.
# Usage: is_version_smaller first_major first_minor first_patch second_major second_minor second_patch
# Returns 0 (true) if the first version is smaller than the second, 1 (false) otherwise.
is_version_smaller() {
    local first_major=$1
    local first_minor=$2
    local first_patch=$3
    local second_major=$4
    local second_minor=$5
    local second_patch=$6

    # Compare major versions
    if [ "$first_major" -lt "$second_major" ]; then
        return 0
    elif [ "$first_major" -gt "$second_major" ]; then
        return 1
    fi

    # Major versions are equal, compare minor versions
    if [ "$first_minor" -lt "$second_minor" ]; then
        return 0
    elif [ "$first_minor" -gt "$second_minor" ]; then
        return 1
    fi

    # Major and minor versions are equal, compare patch versions
    if [ "$first_patch" -lt "$second_patch" ]; then
        return 0
    elif [ "$first_patch" -gt "$second_patch" ]; then
        return 1
    fi

    # Versions are equal
    return 1
}

###########################
### Beginning of script ###
###########################

echo "### EXECUTING VERSION MANAGER ###"

# Check if this is a dry run, indicated by the flag '-d'
dryRun=false

while getopts ":d" opt; do
  case ${opt} in
    d )
      dryRun=true
      ;;
    \? ) echo "Usage: cmd [-d]"
      exit 1
      ;;
  esac
done

if [ "$dryRun" = true ]; then
  echo "Running script in dry run mode."
fi

########################################################
### Determine if any new version needs to be created ###
########################################################

# Determine current branch and check if any actions for versioning are necessary for the branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

if ! [[ "$CURRENT_BRANCH" == "develop" || "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" =~ ^hotfix || "$CURRENT_BRANCH" =~ ^release ]]; then
  echo "No relevant branch for versioning, so there is no new version needed. Exiting."
  exit 1
fi

# Get the commit hash of the latest tag
most_recent_version_tag=$(git tag --list | grep -E '^[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n1)

# No version tag found at all
if [ -z "$most_recent_version_tag" ]; then
    echo "No version tags found. Exiting."
    exit 1
fi

#####################################################
### Create new version and tag most recent commit ###
#####################################################

latest_tag_commit=$(git rev-list -n 1 "$most_recent_version_tag")

# Get the commit hash of the latest commit (HEAD)
latest_commit=$(git rev-parse HEAD)

# Fetch version information from VERSION file and git tags
major_version=$(cat ./version)
echo "Current major version: $major_version"
echo "Most recent version from git tags: $most_recent_version_tag"

# Extract version components
read -r tag_major tag_minor tag_patch tag_suffix <<< "$(extract_version_components "$most_recent_version_tag")"
echo "Extracted major, minor, patch and suffix from most recent tag: $tag_major $tag_minor $tag_patch $tag_suffix"

# Compare the two commit hashes
if [ "$latest_tag_commit" == "$latest_commit" ]; then
    echo "The latest commit is already tagged. No new version needed. Exiting."
    echo "$tag_major.$tag_minor.$tag_patch $tag_suffix"
    exit 0
fi

# Determine if most recent version is smaller than the set major version
is_version_smaller "$tag_major" "$tag_minor" "$tag_patch" "$major_version" 0 0
version_is_smaller=$?

declare new_version
declare suffix

if [[ "$CURRENT_BRANCH" == "develop" ]]; then
    suffix="test"
    if [ $version_is_smaller -eq 0 ]; then
      # New major version
      new_version="$major_version.0.0"
    else
      ((tag_minor++))
      tag_patch="0"
      new_version="$tag_major.$tag_minor.$tag_patch"
    fi
elif [[ "$CURRENT_BRANCH" == "main" ]]; then
    new_version="$tag_major.$tag_minor.$tag_patch"
elif [[ "$CURRENT_BRANCH" =~ ^release- ]]; then
    suffix="beta"
    if [ $version_is_smaller -eq 0 ]; then
      # New major version
      new_version="$major_version.0.0"
    else
      if [[ "$tag_suffix" == "beta" ]]; then
        # Release new beta version with incremented minor version
        ((tag_minor++))
        tag_patch="0"
      fi
      new_version="$tag_major.$tag_minor.$tag_patch"
    fi
elif [[ "$CURRENT_BRANCH" =~ ^hotfix- ]]; then
      ((tag_patch++))
      new_version="$tag_major.$tag_minor.$tag_patch"
else
    echo "Unrecognized branch: $CURRENT_BRANCH. Exiting."
    exit 1
fi

# Create tag and push
declare full_version_string
if [ -n "$suffix" ]; then
  full_version_string="$new_version-$suffix"
else
  full_version_string=$new_version
fi

echo "New version that a tag is created for and pushed: $full_version_string"

if [ "$dryRun" = false ]; then
  git tag "$full_version_string"
  git push origin "$full_version_string"
  echo "Created tag and pushed to the repository."
else
  echo "Skipped creating and pushing tag to the repository because of dry run but captured version $new_version and suffix $suffix"
fi

# Return new version and suffix
echo "$new_version $suffix"
exit 0