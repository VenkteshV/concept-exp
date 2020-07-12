import React, { Component } from "react";
import Dropzone from "./DropZone.jsx";
import Progress from "./Progress.jsx";
import Logo from "../images/baseline-check_circle_outline-24px.svg";
import { Button } from 'react-bootstrap';
import GraphVis from './GraphVis.jsx';
import Hierarchyvis   from './Hierarchyvis.jsx'
import _ from 'lodash';
import Select from 'react-select';
import PropTypes from 'prop-types';


class Upload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      files: [],
      uploading: false,
      uploadProgress: {},
      successfullUploaded: false,
      keywords: {},
      skillname: '',
      bloomVerbs:'',
      bloomtaxonomy:'',
      hierarchy: ''
    };

    this.onFilesAdded = this.onFilesAdded.bind(this);
    this.uploadFiles = this.uploadFiles.bind(this);
    this.sendRequest = this.sendRequest.bind(this);
    this.renderActions = this.renderActions.bind(this);
    this.expandConcepts = this.expandConcepts.bind(this);
    this.handleSkillChange = this.handleSkillChange.bind(this);
    this.getCognitiveComplexity = this.getCognitiveComplexity.bind(this);
    this.getHierarchy = this.getHierarchy.bind(this);

  }

  getCognitiveComplexity() {

    let file = this.state.files[0];
    const req = new XMLHttpRequest();

    let response = {};

    const formData = new FormData();
    formData.append("document", file, file.name);


    req.open("POST", "http://localhost:5000/getcognitivetaxonomy");
    
    // this.props.fetchBloomVerbs({skillname: event})
    req.send(formData);
    let self = this;

    req.onload = function() {
      if (this.readyState == 4 && this.status == 200) {
          console.log(this.responseText);
          response = JSON.parse(this.responseText)
      }
      console.log("bloomtaxonomy", response)
      self.setState({bloomtaxonomy: response})
    }

  }

  handleSkillChange(event){
    this.setState({skillname: event})
    let file = this.state.files[0];
    const req = new XMLHttpRequest();

    let response = {};

    const formData = new FormData();
    formData.append("document", file, file.name);


    req.open("POST", "http://localhost:5000/getbloomverbs/"+ event.value);
    
    // this.props.fetchBloomVerbs({skillname: event})
    req.send(formData);
    let self = this;

    req.onload = function() {
      if (this.readyState == 4 && this.status == 200) {
          console.log(this.responseText);
          response = JSON.parse(this.responseText)
      }
      console.log("response", response)
      self.setState({bloomVerbs: response})
    }
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

  getHierarchy() {
    let file = this.state.files[0];
    const req = new XMLHttpRequest();

    let response = {};

    const formData = new FormData();
    formData.append("document", file, file.name);


    req.open("POST", "http://localhost:5000/predicttaxonomy");
    
    // this.props.fetchBloomVerbs({skillname: event})
    req.send(formData);
    let self = this;

    req.onload = function() {
      if (this.readyState == 4 && this.status == 200) {
          console.log(this.responseText);
          response = JSON.parse(this.responseText)
      }
      console.log("bloomtaxonomy", response)
      self.setState({hierarchy: response})
    }

  }

  render() {
    console.log("bloomtaxonomy", this.state.bloomtaxonomy["bloomtaxonomy"]);
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
      <div className = "cognitive_level">        
        <span className="Title">Select Cognitive complexity level</span>
        <Select key={_.uniqueId()} className="select_skill"
              options={[{ "label": "Knowledge & understanding ", "value": "Understanding" },
               { "label": "Skills & Application", "value": "Applying" }, 
               { "label": "Remembering", "value": "Remembering" },
               { "label": "Applying", "value": "Applying" },
               { "label": "Analysing", "value": "Analysing" },
               { "label": "Evaluating", "value": "Evaluating" },
               { "label": "Creating", "value": "Creating" }]}
              value={this.state.skillname}
              onChange={this.handleSkillChange}
            /></div>
         <div className = "bloom_taxonomy"> 
         <span className="Title"> Infer Cognitive complexity</span>
           <Button onClick = {this.getCognitiveComplexity}
        >
          Cognitive Complexity
        </Button></div>

        <div className = "hierarchy"> 
         <span className="Title"> Get Hierarchy</span>
           <Button onClick = {this.getHierarchy}
        >
          Hierarchical Taxonomy
        </Button></div>
      </div>

      {
          !_.isEmpty(this.state.hierarchy) ?
        (<div> <Hierarchyvis  hierarchy={this.state.hierarchy}/>   </div>) : (null)
        }
       
      <div className="Card">
      {!_.isEmpty( this.state.bloomtaxonomy["bloomtaxonomy"]) ? (
      <div>
      <span className="Title">Matching Cognitive Complexity</span>
      <ul>
            { this.state.bloomtaxonomy["bloomtaxonomy"].map(verb => (
              <li key = {_.uniqueId()}>
                  <div>{verb}</div>
              </li>
            ))}
            </ul> </div>) : (null)}
      </div>
 
      <div className="Card">
      {!_.isEmpty(this.state.bloomVerbs["bloomverbs"]) ? (
      <div>
      <span className="Title">Matching Bloom Verbs</span>
      <ul>
            {this.state.bloomVerbs['bloomverbs'].map(verb => (
              <li key = {_.uniqueId()}>
                  <div>{verb}</div>
              </li>
            ))}
            </ul> </div>) : (null)}
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
Upload.propTypes = {
  fetchBloomVerbs: PropTypes.func,
};

export default Upload;