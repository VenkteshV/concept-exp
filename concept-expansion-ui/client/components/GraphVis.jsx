import Graph from "react-graph-vis";
// import Graph from "../../lib";

// import Graph from 'react-graph-vis'
import PropTypes from 'prop-types';

import React from "react";

export default class GraphVis extends React.Component {
    constructor(props) {
        super(props);

      }

render() {
    let keywords = this.props.keywords;
    console.log("here********************************************", JSON.parse(keywords))
    let keyphrases = JSON.parse(keywords);

    let graph = {};
    graph["nodes"] = [];
    graph["edges"] = [];
    for (let keywordListIndex in keyphrases["keywords"]) {
        console.log("keywordList[0]",keyphrases["keywords"][keywordListIndex])
        if(keywordListIndex <10){
        graph["nodes"].push({id: keywordListIndex, label: keyphrases["keywords"][keywordListIndex][0], color:"#41e0c9"})
        }
        else{
          graph["nodes"].push({id: keywordListIndex, label: keyphrases["keywords"][keywordListIndex][0], color:"#e0df41"})

        }


    }

      
      let options = {
        layout: {
          hierarchical: false
        },
        edges: {
          color: "#000000"
        }
      };

      let events = {
        select: function(event) {
          var { nodes, edges } = event;
          console.log("Selected nodes:");
          console.log(nodes);
          console.log("Selected edges:");
          console.log(edges);
        }
      };
    return(
  <div>
    <Graph graph={graph} options={options} events={events} style={{ height: "640px", width: "640px" }} />
  </div>
);
    }
}

GraphVis.propTypes = {
    keywords: PropTypes.object,
  };