import PropTypes from "prop-types";
/**
 * Created by sean on 03/02/17.
 */
import React from "react";
import { Link } from "react-router-dom";
import classNames from "classnames";
import filesize from "filesize";
import uniq from "lodash/uniq";

import GoFileDirectory from "react-icons/go/file-directory";
import GoFileMedia from "react-icons/go/file-media";
import GoCheck from "react-icons/go/check";
import GoHourglass from "react-icons/go/hourglass";
import FaFileImageO from "react-icons/fa/file-image-o";
import FaFileMovieO from "react-icons/fa/file-movie-o";
import FaFileAudioO from "react-icons/fa/file-audio-o";
import FaChainBroken from "react-icons/fa/chain-broken";

import Breadcrumbs from "../components/breadcrumbs";

require("./index.css");

export class DirectoryListingBreadcrumbs extends React.Component {
  render() {
    let { dirs, current_dir } = this.props;
    let items = dirs.map((d, index) => <Link to={d.link}>{d.name}</Link>);
    return <Breadcrumbs items={items} />;
  }
}

const FilePlaceHolder = ({ mime, className }) => {
  let Icon = GoFileMedia;
  if (mime) {
    let category = mime.split("/")[0];
    switch (category) {
      case "video":
        Icon = FaFileMovieO;
        break;
      case "image":
        Icon = FaFileImageO;
        break;
      case "audio":
        Icon = FaFileAudioO;
        break;
      default:
        break;
    }
  }
  return <Icon title={mime || ""} className={className} />;
};

export class FallBackImageLoader extends React.Component {
  constructor(props) {
    super(props);
    this.handleImageLoadError = this.handleImageLoadError.bind(this);
    this.handleImageLoad = this.handleImageLoad.bind(this);
    this.state = {
      hasError: false,
      hasLoaded: false
    };
  }
  handleImageLoadError(e) {
    this.setState({
      hasError: true
    });
  }

  handleImageLoad(e) {
    this.setState({
      hasLoaded: true
    });
  }
  render() {
    let {
      src,
      alt = "image",
      title = "",
      fallbackImage = FaChainBroken
    } = this.props;
    let { hasError } = this.state;
    if (hasError) {
      let FallBackImage = fallbackImage;
      return <FallBackImage />;
    }
    return (
      <img
        src={src}
        onError={this.handleImageLoadError}
        title={title}
        alt={alt}
      />
    );
  }
}

FallBackImageLoader.propTypes = {
  src: PropTypes.string.isRequired
};

const GGalleryItem = ({
  name,
  preview,
  directory = false,
  selected = false,
  onClick
}) => {
  return (
    <div
      className={classNames("g-gallery-item", {
        selected: selected,
        "g-gallery-item-file": !directory,
        "g-gallery-directory": directory
      })}
      onClick={onClick}
    >
      <span className={classNames("g-gallery-select", { green: selected })}>
        <GoCheck />
      </span>
      {/*<div className='preview'>*/}
      {preview}
      {/*</div>*/}

      <div className="g-gallery-item-name">{name}</div>
    </div>
  );
};

class GGalleryDirectory extends React.Component {
  navigateOrSelect = e => {
    const { navigate, select } = this.props;
    e.ctrlKey ? select(e) : navigate(e);
  };

  render() {
    const { name, navigate, select, selected = false } = this.props;
    return (
      <GGalleryItem
        name={name}
        onClick={this.navigateOrSelect}
        directory={true}
        preview={<GoFileDirectory />}
        selected={selected}
      />
    );
  }
}

export const GGalleryFile = ({ file, toggleSelect, ...props }) => {
  let preview = file.preview_url ? (
    <FallBackImageLoader
      src={file.preview_url}
      title={`${file.name} ${file.mime}`}
      alt="preview image"
    />
  ) : (
    <FilePlaceHolder mime={file.mime} />
  );

  return (
    <GGalleryItem
      onClick={toggleSelect}
      name={file.name}
      preview={preview}
      {...props}
    />
  );
};

const GGalleryUpload = ({ upload }) => {
  return (
    <div className={classNames("g-gallery-item")}>
      <div className="g-gallery-item-preview">
        {upload.preview ? (
          <FallBackImageLoader
            src={upload.preview}
            fallbackImage={GoHourglass}
          />
        ) : null}
      </div>
      <div className="g-gallery-item-name">
        <progress max={100} value={upload.progress}>
          {upload.file}
        </progress>
        <span>{upload.name}</span>
      </div>
    </div>
  );
};

// we can try to extend this in the future to
// enable multiple ways of listing files and directories
const fileListDisplayOptions = {
  tiles: null
};
// exported, because the selected file list type is stored in the state object
export const fileListDisplayValues = Object.keys(fileListDisplayOptions);

export default class FileList extends React.Component {
  constructor(props) {
    super(props);
    this.handleFileSelectEvent = this.handleFileSelectEvent.bind(this);
  }

  handleFileSelectEvent(file, event) {
    let { ctrlKey, shiftKey } = event;
    const key = file.url;
    // start off with a single selected file
    let selection = [key];

    if (ctrlKey || shiftKey) {
      // ctrl + already selected => deselect
      if (ctrlKey && this.props.selectedItemIds.has(key)) {
        selection = Array.from(this.props.selectedItemIds).filter(
          id => key !== id
        );
      } else {
        // else add to selection
        selection = [...this.props.selectedItemIds, ...selection];
      }
    }

    if (shiftKey) {
      // span a selection
      let start = this.allContentIds.indexOf(this.last_selected_id);
      let end = this.allContentIds.indexOf(key);
      let range = [start, end].sort((a, b) => a - b);
      // console.log(`selecting from ${range[0]} to ${range[1]}.`);
      selection = [
        ...selection,
        ...this.allContentIds.slice(range[0], range[1])
      ];
    }
    selection = uniq(selection);
    this.last_selected_id = file.url;
    this.props.handleSelect(selection);
  }

  render() {
    let {
      directories = [],
      files = [],
      uploads = [],
      displayType,
      selectedItemIds,
      handleSelect
    } = this.props;

    if (files.length + directories.length === 0) {
      return null;
    }

    // keep track of all ids in the same order in which they are displayed
    this.allContentIds = [
      ...directories.map(d => d.url),
      ...files.map(f => f.url)
    ];

    let renderedDirectories = directories.map((directory, index) => {
      return (
        <GGalleryDirectory
          {...directory}
          select={this.handleFileSelectEvent.bind(this, directory)}
          key={index}
          selected={selectedItemIds.has(directory.url)}
        />
      );
    });

    let rendererFiles = files.map((file, index) => {
      let props = {
        file: file,
        toggleSelect: this.handleFileSelectEvent.bind(this, file),
        selected: selectedItemIds.has(file.url)
      };
      return <GGalleryFile key={index} {...props} />;
    });

    // let renderedUploads = Object.values(uploads).map((upload, index) => {
    //   return <GGalleryUpload upload={upload} key={index} />;
    // });

    return (
      <div className="g-gallery">
        {renderedDirectories}
        {rendererFiles}
        {/*{renderedUploads}*/}
      </div>
    );
  }
}

export const FileBrowserInterface = ({
  header = null,
  main = null,
  footer = null
}) => {
  return (
    <section className="filebrowser">
      {header ? <header>{header}</header> : null}
      <main>{main}</main>
      {footer ? <footer>{footer}</footer> : null}
    </section>
  );
};
