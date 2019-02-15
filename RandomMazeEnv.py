import logging
import numpy as np
from mlagents.envs import UnityEnvironment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RandomMaze")

class RandomMazeEnv(object):

    def __init__(self, env_file_name):

        self._env = UnityEnvironment(env_file_name)
        self._brain_name = self._env.external_brain_names[0]
        brain = self._env.brains[self._brain_name]

        height = brain.camera_resolutions[0]['height']
        width = brain.camera_resolutions[0]['width']
        action_space = brain.vector_action_space_size[0]

        self._observation_space = (height, width, 3)
        self._action_space = (action_space,)

        self._seed = None

    def reset(self):

        if self._seed is None:
            rseed = np.random.randint(1e6)
        else:
            rseed = self._seed
        assert isinstance(rseed, int), "random seed must be a integer"
        reset_params = dict(RandomSeed = rseed)
        self._env.reset(config = reset_params)[self._brain_name]
        ob, reward, done, info = self.step(np.zeros(self._action_space))
        return ob, reward, done, info

    def step(self, action):

        assert isinstance(action, np.ndarray), "action must be a numpy.ndarry"
        assert action.shape == self._action_space, "action.shape doesn't match env.action_space"

        infos = self._env.step(action)[self._brain_name]
        ob, reward, done, info = self.extract_infos(infos)

        return ob, reward, done, info

    def extract_infos(self, infos):

        ob = infos.visual_observations[0].squeeze()
        reward = infos.rewards[0]
        done = infos.local_done[0]
        info = {}

        return ob, reward, done, info

    def seed(self, seed=None):

        assert isinstance(seed, int), "random seed must be a integer"
        self._seed = seed
        logger.warn("New seed %d will be used after next reset." % self._seed)

    def close(self):
        self._env.close()

    def sample_action(self):
        return np.random.uniform(size=self._action_space)

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def action_space(self):
        return self._action_space
