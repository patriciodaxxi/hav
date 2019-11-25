import React from "react";
import { FiFolder } from "react-icons/fi";

const Folder = ({ name = "Unnamed folder" }) => {
  return (
    <div>
      <FiFolder />
      <p>{name}</p>
    </div>
  );
};

const FileBrowserItem = ({ children }) => {
  return (
    <div
      style={{
        flexGrow: 1,
        flexShrink: 1,
        height: "5rem",
        width: "5rem"
      }}
    >
      {children}
    </div>
  );
};

const FileBrowser = ({ children }) => {
  console.log(children);
  return (
    <div style={{ display: "flex" }}>
      {children.map((child, index) => (
        <FileBrowserItem key={index}>{child}</FileBrowserItem>
      ))}
    </div>
  );
};

export { Folder, FileBrowser };