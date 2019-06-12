import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.train import interactive
from rasa_core.utils import EndpointConfig

logger = logging.getLogger(__name__)


# checkSelfPermission

def run_criminal_online(interpreter,
                          domain_file="data/criminal_domain.yml",
                          training_data_file='data/stories.md'):
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")						  
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=2), 
                  KerasPolicy(max_history=3, epochs=5, batch_size=50)],
                  interpreter=interpreter,
				  action_endpoint=action_endpoint)
    				  
    data = agent.load_data(training_data_file)			   
    agent.train(data)
    interactive.run_interactive_learning(agent, training_data_file)
    return agent

if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/criminalnlu')
    run_criminal_online(nlu_interpreter)