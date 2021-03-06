# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import logging

from qiskit_aqua.algorithms.components.multiclass import multiclass_get_points_and_labels
from qiskit_aqua.algorithms.classical.svm import SVM_Classical_ABC

logger = logging.getLogger(__name__)


class SVM_Classical_Multiclass(SVM_Classical_ABC):
    """
    the multiclass classifier
    the classifier is built by wrapping the estimator (for binary classification) with the multiclass extensions
    """

    def __init__(self, multiclass_classifier):
        self.ret = {}
        self.multiclass_classifier = multiclass_classifier

    def run(self):
        """
        put the train, test, predict together
        """
        if self.training_dataset is None:
            self.ret['error'] = 'training dataset is missing! please provide it'
            return self.ret

        X_train, y_train, label_to_class = multiclass_get_points_and_labels(self.training_dataset, self.class_labels)
        X_test, y_test, label_to_class = multiclass_get_points_and_labels(self.test_dataset, self.class_labels)

        self.multiclass_classifier.train(X_train, y_train)

        if self.test_dataset is not None:
            success_ratio = self.multiclass_classifier.test(X_test, y_test)
            self.ret['test_success_ratio'] = success_ratio

        if self.datapoints is not None:
            predicted_labels = self.multiclass_classifier.predict(X_test)
            predicted_labelclasses = [label_to_class[x] for x in predicted_labels]
            self.ret['predicted_labels'] = predicted_labelclasses
        return self.ret
