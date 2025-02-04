# Copyright 2021 qclib project.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
n-qubit controlled gate
"""
from collections import namedtuple
import numpy as np
import qiskit
from qiskit.circuit import Gate
from qiskit import QuantumCircuit, QuantumRegister
from qclib.gates.util import check_u2, apply_ctrl_state
from qclib.gates.multitargetmcsu2 import MultiTargetMCSU2
from qclib.gates.ldmcu import Ldmcu


# pylint: disable=protected-access
class LogMcx(Gate):
    """
    Toffoli gate with log(n) depth using 2 clean ancilla
    https://arxiv.org/abs/2407.17966

    -----------------------------------------
    Implements gate decomposition of a multi-controlled X operator with 2 clean ancilla
    """

    def __init__(self, num_controls):
        """

        Parameters
        ----------
        num_controls (int): Number of controls
        """

        if num_controls > 0:
            self.control_qubits = QuantumRegister(num_controls)
        else:
            self.control_qubits = []

        self.target_qubit = QuantumRegister(1)
        self.ancilla_qubit = QuantumRegister(2)


    def _define(self):
        if len(self.control_qubits) > 2:
            self.definition = QuantumCircuit(self.target_qubit, self.control_qubits, self.ancilla_qubit)
        elif len(self.control_qubits) == 2:
            self.definition = QuantumCircuit(self.target_qubit, self.control_qubits)
            self.definition.ccx(self.control_qubits[0], self.control_qubits[1], self.target_qubit[0])
        elif len(self.control_qubits) == 1:
            self.definition = QuantumCircuit(self.target_qubit, self.control_qubits)
            self.definition.cx(self.control_qubits[0], self.target_qubit[0])
        else:
            self.definition = QuantumCircuit(self.target_qubit)
            self.definition.ccx(self.target_qubit[0])


    @staticmethod
    def primitive_circuit(n_ctrl, n_target):
        size = n_ctrl + n_target
        qc = QuantumCircuit(size)
        qc.x(list(range(0, n_target)))
        c1 = n_target
        c2 = size - n_target
        for target in range(n_ctrl // 2):
            qc.ccx(c1, c2, target)
            c1 += 1
            c2 += 1
            target += 1
        return qc

