import React, {useState} from 'react';
import './PPOPolicy.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Accordion from 'react-bootstrap/Accordion';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Collapse from 'react-bootstrap/Collapse'

const PPOPolicy = (props) => {
    const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
    const [hParamsOpen, setHParamsOpen] = useState(false);
    const [neuralNetworkDetailsOpen, setNeuralNetworkDetailsOpen] = useState(false);
    const [actionsOpen, setActionsOpen] = useState(false);

    const getAgentTypeStr = (agentType) => {
        if(agentType === 0) {
            return "T-SPSA"
        }
        if(agentType === 1) {
            return "PPO"
        }
        if(agentType === 2) {
            return "T-FP"
        }
        else {
            return "Unknown"
        }
    }

    const getPlayerTypeStr = (playerType) => {
        if(playerType === 1) {
            return "Defender"
        }
        if(playerType === 2) {
            return "Attacker"
        }
        else {
            return "Unknown"
        }
    }

    const renderRemovePPOPolicy = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove PPO policy
        </Tooltip>
    );

    return (<Card key={props.policy.id} ref={props.wrapper}>
        <Card.Header>
            <Accordion.Toggle as={Button} variant="link" eventKey={props.policy.id} className="mgHeader">
                <span
                    className="subnetTitle">ID: {props.policy.id}, Simulation: {props.policy.simulation_name},
                    Average reward: {props.policy.avg_R}</span>
            </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey={props.policy.id}>
            <Card.Body>
                <h5 className="semiTitle">
                    Actions:
                    <OverlayTrigger
                        className="removeButton"
                        placement="left"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemovePPOPolicy}
                    >
                        <Button variant="danger" className="removeButton"
                                onClick={() => props.removePPOPolicy(props.policy)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </h5>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                            aria-controls="generalInfoBody"
                            aria-expanded={generalInfoOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> General Information about the policy </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={generalInfoOpen}>
                        <div id="generalInfoBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Attribute</th>
                                        <th> Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <td>ID</td>
                                        <td>{props.policy.id}</td>
                                    </tr>
                                    <tr>
                                        <td>Simulation name</td>
                                        <td>{props.policy.simulation_name}</td>
                                    </tr>
                                    <tr>
                                        <td>Average reward</td>
                                        <td>{props.policy.avg_R}</td>
                                    </tr>
                                    <tr>
                                        <td>Agent type</td>
                                        <td>{getAgentTypeStr(props.policy.agent_type)}</td>
                                    </tr>
                                    <tr>
                                        <td>Player type</td>
                                        <td>{getPlayerTypeStr(props.policy.player_type)}</td>
                                    </tr>
                                    <tr>
                                        <td>Save path</td>
                                        <td>{props.policy.save_path}</td>
                                    </tr>
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setHParamsOpen(!hParamsOpen)}
                            aria-controls="hyperparametersBody"
                            aria-expanded={hParamsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Hyperparameters </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={hParamsOpen}>
                        <div id="hyperparametersOpen" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Description</th>
                                        <th>Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {Object.keys(props.policy.experiment_config.hparams).map((hparamName, index) => {
                                        return <tr key={hparamName + "-" + index}>
                                            <td>{hparamName}</td>
                                            <td>{props.policy.experiment_config.hparams[hparamName].descr}</td>
                                            <td>{props.policy.experiment_config.hparams[hparamName].value}</td>
                                        </tr>
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setNeuralNetworkDetailsOpen(!neuralNetworkDetailsOpen)}
                            aria-controls="neuralNetworkDetailsBody"
                            aria-expanded={neuralNetworkDetailsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Neural network architecture </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={neuralNetworkDetailsOpen}>
                        <div id="neuralNetworkDetailsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Property</th>
                                        <th> Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <td>Num hidden layers:</td>
                                        <td>{props.policy.policy_kwargs.net_arch.length}</td>
                                    </tr>
                                    {props.policy.policy_kwargs.net_arch.map((layer, index) => {
                                        return (<tr key={layer + "-" + index}>
                                            <td>Num neurons for hidden layer: {index}</td>
                                            <td>{layer}</td>
                                        </tr>)
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

                <Card>
                    <Card.Header>
                        <Button
                            onClick={() => setActionsOpen(!actionsOpen)}
                            aria-controls="actionsBody"
                            aria-expanded={actionsOpen}
                            variant="link"
                        >
                            <h5 className="semiTitle"> Actions </h5>
                        </Button>
                    </Card.Header>
                    <Collapse in={actionsOpen}>
                        <div id="actionsBody" className="cardBodyHidden">
                            <div className="table-responsive">
                                <Table striped bordered hover>
                                    <thead>
                                    <tr>
                                        <th>Action ID</th>
                                        <th> Description</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {props.policy.actions.map((action, index) => {
                                        return <tr key={action + "-" + index}>
                                            <td>{action.id}</td>
                                            <td>{action.descr}</td>
                                        </tr>
                                    })}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </Collapse>
                </Card>

            </Card.Body>
        </Accordion.Collapse>
    </Card>)
}

PPOPolicy.propTypes = {};
PPOPolicy.defaultProps = {};
export default PPOPolicy;
