import React, { Component } from "react";
import Dropzone from "./DropZone.jsx";
import Progress from "./Progress.jsx";
import Logo from "../images/baseline-check_circle_outline-24px.svg";
import { Button } from 'react-bootstrap';
import GraphVis from './GraphVis.jsx';
import _ from 'lodash';


class Upload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      files: [],
      uploading: false,
      uploadProgress: {},
      successfullUploaded: false,
      keywords: {},
    };

    this.onFilesAdded = this.onFilesAdded.bind(this);
    this.uploadFiles = this.uploadFiles.bind(this);
    this.sendRequest = this.sendRequest.bind(this);
    this.renderActions = this.renderActions.bind(this);
    this.expandConcepts = this.expandConcepts.bind(this);
  }

  onFilesAdded(files) {
    this.setState(prevState => ({
      files: prevState.files.concat(files)
    }));
  }

  async uploadFiles() {
    this.setState({ uploadProgress: {}, uploading: true });
    const promises = [];
    this.state.files.forEach(file => {
      promises.push(this.sendRequest(file, false));
    });
    try {
      await Promise.all(promises);

      this.setState({ successfullUploaded: true, uploading: false });
    } catch (e) {
      // Not Production ready! Do some error handling here instead...
      this.setState({ successfullUploaded: true, uploading: false });
    }
  }


  async expandConcepts() {
    const promises = [];

    this.state.files.forEach(file => {
      promises.push(this.sendRequest(file,true));
    });
    try {
      await Promise.all(promises);

      this.setState({ successfullUploaded: true, uploading: false });
    } catch (e) {
      // Not Production ready! Do some error handling here instead...
      this.setState({ successfullUploaded: true, uploading: false });
    }
  }



  sendRequest(file, isExpand) {
    return new Promise((resolve, reject) => {
      const req = new XMLHttpRequest();
      let response = {};

      req.upload.addEventListener("progress", event => {
        if (event.lengthComputable) {
          const copy = { ...this.state.uploadProgress };
          copy[file.name] = {
            state: "pending",
            percentage: (event.loaded / event.total) * 100
          };
          this.setState({ uploadProgress: copy });
        }
      });

      req.upload.addEventListener("load", event => {
        const copy = { ...this.state.uploadProgress };
        copy[file.name] = { state: "done", percentage: 100 };
        this.setState({ uploadProgress: copy });
        resolve(req.response);
      });

      req.upload.addEventListener("error", event => {
        const copy = { ...this.state.uploadProgress };
        copy[file.name] = { state: "error", percentage: 0 };
        this.setState({ uploadProgress: copy });
        reject(req.response);
      });

      let self = this;

      req.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            response = this.responseText
        }
        self.setState({keywords: response})
        console.log("fnskjfkf", self.state.keywords);

    };


 

      const formData = new FormData();
      formData.append("document", file, file.name);


      if(isExpand) {
        req.open("POST", "http://localhost:5000/concept/expand");
      }
      else{
      req.open("POST", "http://localhost:5000/concept/extract");
      }      req.send(formData);
    });
  }

  renderProgress(file) {
    const uploadProgress = this.state.uploadProgress[file.name];
    if (this.state.uploading || this.state.successfullUploaded) {
      return (
        <div className="ProgressWrapper">
          <Progress progress={uploadProgress ? uploadProgress.percentage : 0} />
          <img
            className="CheckIcon"
            alt="done"
            src={Logo}
            style={{
              opacity:
                uploadProgress && uploadProgress.state === "done" ? 0.5 : 0
            }}
          />
        </div>
      );
    }
  }

  renderActions() {
    if (this.state.successfullUploaded) {
      return (
        <Button
          onClick={() =>
            this.setState({ files: [], successfullUploaded: false })
          }
        >
          Clear
        </Button>
      );
    } else {
      return (
        <Button
          disabled={this.state.files.length < 0 || this.state.uploading}
          onClick={this.uploadFiles}
        >
          Upload
        </Button>
      );
    }
  }

  render() {
    return (
      <div className="UploadFile">
      <div className="Card">
      <div className="Upload">
        <span className="Title">Upload Files</span>
        <div className="Content">
          <div>
            <Dropzone
              onFilesAdded={this.onFilesAdded}
              disabled={this.state.uploading || this.state.successfullUploaded}
            />
          </div>
          <div className="Files">
            {this.state.files.map(file => {
              return (
                <div key={file.name} className="Row">
                  <span className="Filename">{file.name}</span>
                  {this.renderProgress(file)}
                </div>
              );
            })}
          </div>
        </div>
        <div className="Actions">{this.renderActions()}</div>
      </div>
      </div>
      {
          !_.isEmpty(this.state.keywords) ?
        (<div> <GraphVis  keywords={this.state.keywords}/>         <Button onClick = {this.expandConcepts}
        >
          Expand Concepts
        </Button></div>) : (null)
        }
    </div>
    );
  }
}

export default Upload;