import _ from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';
// import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
// import SearchComponent from './SelectorComponent.jsx/index.js';
import Select from 'react-select';
import Logo from '../images/gp.png';

export default class JvmtunerComponent extends React.Component {
  /* istanbul ignore next */
  constructor(props) {
    super(props);
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleExpSelectChange = this.handleExpSelectChange.bind(this);
    this.handleWorkloadChange = this.handleWorkloadChange.bind(this);
    this.handleGcFlagChange = this.handleGcFlagChange.bind(this);
    this.handleMetricChange = this.handleMetricChange.bind(this);
    this.handleBenchMarkChange = this.handleBenchMarkChange.bind(this);
    this.state = {
      selectedExp: [],
      workload: [],
      gc_flag: '',
      metric: '',
      benchmark: ''
    };
  }

  handleClick() {
    this.props.runExperiment(this.props.selectedValues, this.state.selectedExp, this.state.workload, this.state.metric, this.state.benchmark);
  }

  handleSearchChange(event) {
    this.props.searchConditions(event);
  }

  handleBenchMarkChange(event) {
    this.setState({benchmark: event});
  }
  handleWorkloadChange(event) {
    this.setState({ workload: event });
    this.props.searchConditions({ workload: event, gc_flag: this.state.gc_flag, metric: this.state.metric, benchmark: this.state.benchmark});
  }


  handleExpSelectChange(event) {
    this.setState({ selectedExp: event });
  }

  handleGcFlagChange(event) {
    this.setState({ gc_flag: event })
  }

  handleMetricChange(event) {
    this.setState({ metric: event })
  }
  render() {
    console.log('values', this.props.selectedValues);
    console.log("this.state.workload", this.state.gc_flag)
    console.log("this.props.config", this.props.config)
    return (
      <div>
        <img src={Logo} />
        <div className="decideexp">

          <div>
            <span><h2>Select benchmark to tune</h2> </span>
            <Select key={_.uniqueId()} className="select"
              options={[{ "label": "dacapo", value: "dacapo" },
              { "label": "HiBench", "value": "HiBench" }
              ]}
              value={this.state.benchmark}
              onChange={this.handleBenchMarkChange}
            />
          </div>
          <div>
            <span><h2>Select metric to tune</h2> </span>
            <Select key={_.uniqueId()} className="select"
              options={[{ "label": "latency", value: "latency" },
              { "label": "HeapUsage", "value": "HeapUsage" },
              { "label": "ClassLoadRate", "value": "ClassLoadRate" },
              { "label": "CompilationRate", "value": "CompilationRate" }

              ]}
              value={this.state.metric}
              onChange={this.handleMetricChange}
            />
          </div>
          <div>
            <span><h2>Select GC mode</h2> </span>
            <Select key={_.uniqueId()} className="select"
              options={[{ "label": "UseSerialGC", value: "UseSerialGC" },
              { "label": "UseParallelOldGC", "value": "UseParallelOldGC" },
              { "label": "UseParallelGC", "value": "UseParallelGC" },
              { "label": "UseConcMarkSweepGC", "value": "UseConcMarkSweepGC" },
              { "label": "UseParNewGC", "value": "UseParNewGC" },
              { "label": "UseG1GC", "value": "UseG1GC" }

              ]}
              value={this.state.gc_flag}
              onChange={this.handleGcFlagChange}
            />
          </div>

          <span><h2>Select workload</h2> </span>
          <div className="experiment">
            <Select key={_.uniqueId()} className="select"
              options={[{ "label": "h2", value: "h2" }, { "label": "LDAExample", "value": "LDAExample" }, { "label": "eclipse", "value": "eclipse" }, { "label": "avrora", "value": "avrora" }]}
              value={this.state.workload}
              onChange={this.handleWorkloadChange}
            />
          </div>
          <div>
            <span><h2>Select flags to tune</h2> </span>
            <Select key={_.uniqueId()} className="select"
              options={this.props.config.config}
              value={this.props.selectedValues}
              onChange={this.handleSearchChange}
              isMulti
            />
          </div>
          <span><h2>Select optimization method</h2> </span>
          <div className="experiment">
            <Select key={_.uniqueId()} className="select"
              options={[{ "label": "bayesopt", value: "bayesopt" }, { "label": "annealing", "value": "annealing" }]}
              value={this.state.selectedExp}
              onChange={this.handleExpSelectChange}
            />
          </div>

        </div>
        <Button bsStyle="success" onClick={this.handleClick}>Submit</Button>
      </div>
    )
  }
}
JvmtunerComponent.propTypes = {
  config: PropTypes.object,
  selectedValues: PropTypes.object,
  searchConditions: PropTypes.func,
  runExperiment: PropTypes.func,
};
