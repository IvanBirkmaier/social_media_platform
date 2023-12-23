import { Button } from "@/components/ui/button";
import React, { useCallback, useState } from "react";
import { FileWithPath, useDropzone } from "react-dropzone";

type AddPostProps = {
  fieldChange: (files: File[]) => void;
  mediaUrl: string;
};

const AddPost = ({ fieldChange = () => {}, mediaUrl }: AddPostProps) => {
  const convertFileToUrl = (file: File) => URL.createObjectURL(file);

  const [file, setFile] = useState<File[]>([]);
  const [fileUrl, setFileUrl] = useState<string>(mediaUrl);
  const [description, setDescription] = useState("");
  const onDrop = useCallback(
    (acceptedFiles: FileWithPath[]) => {
      setFile(acceptedFiles);
      fieldChange(acceptedFiles);
      setFileUrl(convertFileToUrl(acceptedFiles[0]));
    },
    [file]
  );

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpeg", ".jpg"],
    },
  });

  const handleSubmit = () => {
    // Implementiere hier die Logik zum Erstellen und Speichern des Posts
    // Beispiel: Hochladen des Bildes und der Beschreibung an einen Server
    console.log("Post wird hochgeladen:", file, description);
    // Weitere Logik zum Speichern des Posts
  };

  return (
    <div className="flex flex-1">
      <div className="common-container">
        <div className="max-w-5xl flex-start gap-3 justify-start w-full">
          <h2 className="h3-bold md:h2-bold text-left w-full">Add Post</h2>
          {/* Button zum Hochladen des Posts */}
        <Button
          type="button" 
          className="shad-button_dark_4"
          onClick={handleSubmit}
        >
          Upload
        </Button>
        </div>
        <div className="flex flex-row gap-4">
          {/* <PostForm action="Create" /> */}
        <div
          {...getRootProps()}
          className="flex flex-center flex-col bg-dark-3 rounded-xl cursor-pointer"
        >
          <input {...getInputProps()} className="cursor-pointer" />

          {fileUrl ? (
            <>
              <div className="flex flex-1 justify-center w-full p-5 lg:p-10">
                <img src={fileUrl} alt="image" className="file_uploader-img" />
              </div>
              <p className="file_uploader-label">
                Click or drag photo to replace
              </p>
            </>
          ) : (
            <div className="file_uploader-box ">
              <img
                src="/assets/icons/file-upload.svg"
                width={96}
                height={77}
                alt="file upload"
              />

              <h3 className="base-medium text-light-2 mb-2 mt-6">
                Drag photo here
              </h3>
              <p className="text-light-4 small-regular mb-6">SVG, PNG, JPG</p>

              <Button type="button" className="shad-button_dark_4">
                Select from computer
              </Button>
            </div>
          )}
        </div>
        {/* Textfeld für die Beschreibung */}
        <textarea
          className="description-textarea"
          placeholder="Enter description here..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

        </div>

        
    </div>
  );
};

export default AddPost;
