/**
 * Created by sean on 09/02/17.
 */
import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

import { createDirectoryAction, selectItems } from "../../ducks/browser";
import {
  switchFilebrowserDisplayType,
  switchGrouped
} from "../../ducks/settings";
import { queueForIngestion } from "../../ducks/ingest";
import { startFileUpload } from "../../ducks/uploads";
import { LoadingPage } from "../../ui/loading";

import BreadCrumbs from "./breadcrumbs";

import Level, { LevelItem } from "../../ui/components/level";

import FileList, { FileBrowserInterface } from "../../ui/filebrowser";

import {
  FileBrowserMenu,
  SelectedFilesControls
} from "../../ui/filebrowser/controls";
import { buildFrontendUrl } from "../../api/urls";
import buildAPIUrl from "../../routes";
import groupFiles from "./grouping";

class FileBrowserDirectory extends React.Component {
  render() {
    if (this.props.loading) {
      return <LoadingPage />;
    } else {
      const {
        directory,
        childrenDirectories,
        files,
        groupedFiles,
        settings,
        switchDisplayStyle,
        allowUpload,
        uploadFile,
        allowCreate,
        saveFileSelection,
        createDirectory,
        selectItems,
        ingestable,
        toggleGrouped
      } = this.props;

      let uploads = this.props.uploads;
      let breadcrumbs = <BreadCrumbs directory={directory} />;

      // spice up the directories
      let directories = childrenDirectories.map(d => {
        return {
          ...d,
          navigate: () => {
            this.props.history.push(buildFrontendUrl(d.url));
          }
        };
      });

      let isEmpty =
        childrenDirectories.length + files.length + uploads.length === 0;

      const selectedItemIds = new Set(directory.selected);
      const header = (
        <Level
          key="fb-menu"
          left={
            <h1 key="title" className="title">
              {directory.name}
            </h1>
          }
          right={
            <FileBrowserMenu
              switchDisplayType={switchDisplayStyle}
              selectedDisplayType={settings.selectedDisplayType}
              addDirectory={allowCreate}
              selectedItemIds={Array.from(ingestable)}
              allItemIds={directory.content}
              handleSelect={selectItems}
              saveFileSelection={() =>
                saveFileSelection(Array.from(ingestable))
              }
              allowUpload={allowUpload}
              uploadFile={uploadFile}
              toggleGrouped={toggleGrouped}
              isGrouped={settings.displayGrouped}
            />
          }
        />
      );

      const main = isEmpty ? (
        <h2>This directory is empty.</h2>
      ) : (
        <FileList
          directories={directories}
          files={files}
          groupedFiles={groupedFiles}
          uploads={uploads}
          displayType={settings.selectedDisplayType}
          handleSelect={selectItems}
          selectedItemIds={selectedItemIds}
          settings={settings}
        />
      );

      let footer = this.props.footer;
      if (!footer && selectedItemIds.size > 0) {
        footer = (
          <footer className="box">
            <Level
              right={
                <LevelItem>
                  {" "}
                  <SelectedFilesControls
                    save={() => saveFileSelection(Array.from(selectedItemIds))}
                    text={
                      selectedItemIds.size === 1
                        ? "Ingest one item"
                        : `Ingest ${selectedItemIds.size} items`
                    }
                  />
                </LevelItem>
              }
            />
          </footer>
        );
      }

      return (
        <FileBrowserInterface
          header={header}
          breadcrumbs={breadcrumbs}
          main={main}
          footer={footer}
        />
      );
    }
  }
}

FileBrowserDirectory.propTypes = {
  files: PropTypes.array,
  directory: PropTypes.object.isRequired,
  childrenDirectories: PropTypes.array,
  switchDisplayStyle: PropTypes.func.isRequired,
  settings: PropTypes.object,
  saveFileSelection: PropTypes.func,
  allowUpload: PropTypes.bool,
  uploadFile: PropTypes.func,
  allowCreate: PropTypes.bool
};

const FileBrowserDirectoryView = connect(
  (rootState, props) => {
    const state = rootState.repositories;
    const uploadState = rootState.uploads;
    const settings = rootState.settings;
    const { path } = props.match.params;

    const key = buildAPIUrl(props.match.params);

    let directory = props.data;
    let mappedProps = {
      directory,
      path
    };

    const allChildren = (directory.content || []).map(c => state[c]);

    // populate children dirs and files from state
    const childrenDirectories = allChildren.filter(c => c.isDirectory);
    const files = allChildren.filter(c => c.isFile);
    // optionally group files
    const groupedFiles = settings.displayGrouped ? groupFiles(files) : {};
    // get a list of all ingestable and selected items
    const selected = new Set(directory.selected);
    const ingestable = allChildren
      .filter(f => selected.has(f.url) && f.ingestable)
      .map(f => f.url);

    // get the un-finished uploads for directory
    let directoryUploads = Object.values(uploadState[key] || []).filter(
      u => !u.finished
    );
    return {
      ...mappedProps,
      loading: false,
      directory,
      uploads: directoryUploads,
      settings,
      childrenDirectories,
      files,
      groupedFiles,
      ingestable,
      allowUpload: directory.allowUpload || false,
      allowCreate: directory.allowCreate || false
    };
  },
  (dispatch, props) => {
    const apiURL = buildAPIUrl(props.match.params);
    const saveFileSelection = ids => {
      dispatch(queueForIngestion(ids));
    };

    return {
      saveFileSelection,
      uploadFile: file => dispatch(startFileUpload(file, apiURL)),
      switchDisplayStyle: style =>
        dispatch(switchFilebrowserDisplayType(style)),
      toggleGrouped: () => dispatch(switchGrouped()),
      createDirectory: name => dispatch(createDirectoryAction(name, apiURL)),
      selectItems: (items = []) => dispatch(selectItems(apiURL, items))
    };
  }
)(FileBrowserDirectory);

FileBrowserDirectoryView.propTypes = {
  data: PropTypes.object
};

export default FileBrowserDirectoryView;
