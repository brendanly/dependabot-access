import json
import unittest
from unittest.mock import patch, mock_open, ANY

from dependabot_access.access import App, configure_app, convert_access_config


class TestArgs(unittest.TestCase):

    @patch('dependabot_access.access.App')
    def test_args(self, patch_app):

        # given
        access = [{'repos': ['test'], 'teams': {}}]
        with patch(
            'dependabot_access.access.open',
            mock_open(read_data=json.dumps(access)),
            create=True
        ) as mocked_open:
            with patch.dict(
                'dependabot_access.access.os.environ',
                {'GITHUB_TOKEN': 'test-github-token'}
            ):
                # when
                configure_app([
                    '--org', 'test-org',
                    '--team', 'test-team',
                    '--access', 'test-file.json',
                    '--dependabot-id', '123456',
                    '--account-id', '7890'
                ], 'test-github-token')

            # then
            patch_app.assert_called_once_with(
                'test-org', 'test-team', 'test-github-token', '123456',
                '7890', ANY
            )
            mocked_open.assert_called_once_with('test-file.json', 'r')
            patch_app.return_value.run.assert_called_once_with({
                'test': {'teams': {}, 'apps': {}}
            })


class TestFormatConversion(unittest.TestCase):

    def test_array_conversion(self):
        self.assertEqual(
            convert_access_config([
                {
                    'teams': {'team-a': 'pull', 'team-b': 'push'},
                    'repos': ['repo-a', 'repo-b']
                },
                {
                    'teams': {'team-c': 'pull'},
                    'repos': ['repo-c']
                },
                {
                    'teams': {'team-c': 'pull'},
                    'apps': {'dependabot': True},
                    'repos': ['repo-d']
                },
            ], 'test-main-team'),
            {
                'repo-a': {
                    'teams': {'team-a': 'pull', 'team-b': 'push'},
                    'apps': {}
                },
                'repo-b': {
                    'teams': {'team-a': 'pull', 'team-b': 'push'},
                    'apps': {}
                },
                'repo-c': {
                    'teams': {'team-c': 'pull'},
                    'apps': {}
                },
                'repo-d': {
                    'teams': {'team-c': 'pull'},
                    'apps': {'dependabot': True}
                }
            }
        )


class TestDependabotConfiguration(unittest.TestCase):

    def test_access_granted_for_app_github(self):
        pass
        access_config = {
            'test-repo': {
                'teams': {},
                'apps': {
                    'dependabot': 'true'
                }
            }
        }
        App.configure()