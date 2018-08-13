import React from "react";
import filesize from "filesize";
import { FallBackImageLoader } from "./index";
import Button from "../components/buttons";

export default class extends React.Component {
  render() {
    const props = this.props;
    const tableProps = {
      Size: filesize(this.props.size),
      "Mime Type": this.props.mime,
      Ingestable: this.props.ingestable
    };
    return (
      <div className="container content">
        <h1>{this.props.name}</h1>
        <hr />
        <div>
          <FallBackImageLoader
            sources={this.props.srcset}
            mime_type={props.mime_type}
            alt={props.name}
          />
        </div>
        <h2>Properties</h2>
        <Button onClick={props.ingest} className="is-primary">
          Ingest
        </Button>
        <table className="table is-striped">
          <tbody>
            {Object.entries(tableProps).map(([key, value]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <pre>{JSON.stringify(this.props, null, 2)}</pre>
      </div>
    );
  }
}