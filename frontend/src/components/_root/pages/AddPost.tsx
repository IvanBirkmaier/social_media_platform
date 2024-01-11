import { Button } from "@/components/ui/button";
import { useCallback, useState } from "react";
import { FileWithPath, useDropzone } from "react-dropzone";
import { useAuth } from "@/components/Auth/AuthContext";
import { backendUrl } from "@/utils/utils";
import fileUploadIcon from "assets/icons/file-upload.svg";

type AddPostProps = {
  fieldChange?: (files: File[]) => void;
  mediaUrl?: string;
};

const AddPost = ({ fieldChange, mediaUrl }: AddPostProps) => {
  //const navigate = useNavigate();
  const { user } = useAuth();
  const convertFileToUrl = (file: File) => URL.createObjectURL(file);

  const [file, setFile] = useState<File[]>([]);
  const [fileUrl, setFileUrl] = useState<string>(mediaUrl || "");
  const [description, setDescription] = useState("");

  const onDrop = useCallback(
    (acceptedFiles: FileWithPath[]) => {
      setFile(acceptedFiles);
      if (fieldChange) {
        fieldChange(acceptedFiles);
      }
      setFileUrl(convertFileToUrl(acceptedFiles[0]));
    },
    [file, fieldChange]
  );

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpeg", ".jpg"],
    },
  });

  // Hilfsfunktion, um Dateien in Base64 zu konvertieren
  const toBase64 = (file: File) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });

  const handleSubmit = async () => {
    if (file.length > 0) {
      try {
        const base64Image = await toBase64(file[0]);
        const postPayload = {
          account_id: user?.id || 0,
          description: description,
          base64_image: base64Image,
        };

        // Ersetze 'http://localhost:8000' mit der URL deines FastAPI-Servers
        const response = await fetch(`${backendUrl}/posts/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(postPayload),
        });
        console.log(response);
        if (response.ok) {
          console.log("Post erfolgreich erstellt");
          // Zusätzliche Logik nach erfolgreichem Upload
        } else {
          console.error("Fehler beim Erstellen des Posts");
        }

        // Zustände zurücksetzen
        setFile([]);
        setFileUrl("");
        setDescription("");
      } catch (error) {
        console.error("Fehler beim Hochladen des Posts:", error);
      }
    } else {
      alert("Please select an image.");
    }
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
                  <img
                    src={fileUrl}
                    alt="image"
                    className="file_uploader-img"
                  />
                </div>
                <p className="file_uploader-label">
                  Click or drag photo to replace
                </p>
              </>
            ) : (
              <div className="file_uploader-box ">
                <img
                  src={fileUploadIcon}
                  width={96}
                  height={77}
                  alt="file upload"
                />

                <h3 className="base-medium text-light-2 mb-2 mt-6">
                  Drag photo here
                </h3>
                <p className="text-light-4 small-regular mb-6">JPG, PNG</p>

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
