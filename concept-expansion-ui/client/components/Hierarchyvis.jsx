import Graph from "react-graph-vis";
// import Graph from "../../lib";

// import Graph from 'react-graph-vis'
import PropTypes from 'prop-types';

import React from "react";

export default class Hierarchyvis extends React.Component {
    constructor(props) {
        super(props);

      }

render() {
    let hierarchy = this.props.hierarchy;
    let keyphrases = hierarchy;

    let graph = {};
    graph["nodes"] = [];
    graph["edges"] = [];
    let hierarchy_list = keyphrases["subjecttaxonomy"].slice(0,5)
    // console.log("graph", graph);
    for (let keywordListIndex in hierarchy_list) {
        let nextIndex = eval(keywordListIndex)+eval(1)
        // console.log("keywordList[0]",hierarchy_list[keywordListIndex])
        graph["nodes"].push({id: keywordListIndex, label: hierarchy_list[keywordListIndex], color:"#41e0c9", height:"90px"});
        graph["edges"].push({from: keywordListIndex, to: nextIndex });
    }

      
      let options = {
        layout: {
          hierarchical: true
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
    <Graph graph={graph} options={options} events={events} style={{ height: "740px", width: "740px" }} />
  </div>
);
    }
}

Hierarchyvis.propTypes = {
    hierarchy: PropTypes.object,
  };
