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
    let hierarchy_list = keyphrases["bloomtaxonomy"].split(">>")
    console.log("graph", graph);
    for (let keywordListIndex in hierarchy_list) {
        let nextIndex = eval(keywordListIndex)+eval(1)
        console.log("keywordList[0]",hierarchy_list[keywordListIndex],hierarchy_list[nextIndex],nextIndex, keywordListIndex)
        graph["nodes"].push({id: keywordListIndex, label: hierarchy_list[keywordListIndex], color:"#41e0c9"});
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
    <Graph graph={graph} options={options} events={events} style={{ height: "640px", width: "640px" }} />
  </div>
);
    }
}

Hierarchyvis.propTypes = {
    hierarchy: PropTypes.object,
  };