import os

import allure
import pytest
from test_api.base import ApiBase


class WrongLogicTypeException(Exception):
    pass


class SegmentsApi(ApiBase):
    @allure.step('Creating segment {segment_name}')
    def create_segment(self, segment_name, logic_type='or', pass_condition=None):
        relations = [
            {
                'object_type': "remarketing_player",
                'params': {
                    'type': "positive",
                    'left': 150,
                    'right': 25
                }
            },
            {
                'object_type': "remarketing_payer",
                'params': {
                    'type': "positive",
                    'left': 170,
                    'right': 10
                }
            }
        ]

        if logic_type == 'or':
            pass_condition = 1
        elif logic_type == 'and':
            pass_condition = len(relations)
        elif logic_type == 'not':
            pass_condition = 0
        elif logic_type != 'rule':
            raise WrongLogicTypeException

        payload = {
            'logicType': logic_type,
            'name': segment_name,
            'pass_condition': pass_condition,
            'relations': relations
        }

        segment_id = self.api_client.post_segment_create(payload)
        return segment_id

    def check_if_segment_exists(self, segment_id):
        return segment_id in self.api_client.get_segments_ids_list()
