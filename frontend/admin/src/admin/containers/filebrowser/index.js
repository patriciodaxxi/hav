/**
 * Created by sean on 09/02/17.
 */
import React from "react";
import { connect } from "react-redux";

import { requestDirectoryAction } from "../../ducks/browser";

import { LoadingPage } from "../../ui/loading";

import buildApiUrl from "../../routes";

import DirectoryView from "./folder";
import FileView from "./detail";

class FilebrowserView extends React.Component {
  componentDidMount() {
    this.props.loadData();
  }

  UNSAFE_componentWillReceiveProps(newProps) {
    if (newProps.match.url !== this.props.match.url) {
      newProps.loadData();
    }
  }

  render() {
    if (this.props.loading) {
      return <LoadingPage />;
    }
    return this.props.data.isFile ? (
      <FileView {...this.props} />
    ) : (
      <DirectoryView {...this.props} />
    );
  }
}

export default connect(
  (state, props) => {
    const key = buildApiUrl(props.match.params);
    const data = state.repositories[key];
    return {
      loading: data == undefined,
      data: data
    };
  },
  (dispatch, props) => {
    const apiURL = buildApiUrl(props.match.params);
    return {
      loadData: () => {
        dispatch(requestDirectoryAction(apiURL));
      }
    };
  }
)(FilebrowserView);
