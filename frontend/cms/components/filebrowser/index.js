import React from "react";

import { MdFolder as FolderIcon } from "react-icons/md";

import styles from "./filebrowser.module.css";

const Media = ({ title, thumbnailUrl }) => {
  return (
    <div className={styles.item}>
      <img src={thumbnailUrl} alt={title} />
      <p>{title}</p>
    </div>
  );
};

const Folder = ({ name = "Unnamed folder" }) => {
  return (
    <div className={styles.item}>
      <FolderIcon />
      <p>{name}</p>
    </div>
  );
};

const FileBrowser = ({ children }) => {
  return <div className={styles.filebrowser}>{children}</div>;
};

export { Folder, Media, FileBrowser };
