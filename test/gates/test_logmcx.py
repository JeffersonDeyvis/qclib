#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Test qclib.gate.log_mcx_gate """

from unittest import TestCase
from qiskit.quantum_info import Operator, Statevector
import numpy as np
from qiskit import QuantumCircuit
from qclib.gates.logmcx import LogMcx

class TestLogToffoli(TestCase):
    """ Testing qclib.gate.logmcx """

    def test_zero_controls(self):


        num_controls = 0
        log_mcx = LogMcx(num_controls)
        log_mcx._define()

        self.assertEqual(log_mcx.definition.num_qubits, 1)

        ops = log_mcx.definition.count_ops()
        self.assertEqual(ops.get('x', 0), 1)

    def test_primitive_circuit_count_gates(self):

        rng_n_ctrls = np.random.randint(2, 10)
        n_targets = rng_n_ctrls // 2
        qc = LogMcx.primitive_circuit(rng_n_ctrls, n_targets)

        self.assertEqual(qc.count_ops().get('x', 0), n_targets)
        self.assertEqual(qc.count_ops().get('ccx', 0), n_targets)


    def test_circuit_one_dirty_ancilla(self):
        n_controls = 9
        target = [0]
        qc1 = LogMcx.circuit_one_dirty_ancilla(n_controls)
        qc2 = QuantumCircuit(n_controls+2)
        qc2.mcx(list(range(1, n_controls+1)), target)

        u2 = Operator(qc2).data
        u1 = Operator(qc1).data

        self.assertTrue(np.allclose(u2, u1))


    def test_circuit_one_clean_ancilla(self):

        n_controls = 9
        target = [0]
        n = n_controls + 1
        qc1 = QuantumCircuit(n)
        qc1.mcx(list(range(1, n)), target)
        qc2 = LogMcx.circuit_one_dirty_ancilla(n_controls)
        ket_zero = Statevector.from_label('0')

        op1 = Operator(qc1).data
        op2 = Operator(qc2).data

        for k in range(2 ** n):

            # base state |K>
            input_data = Statevector.from_int(k, dims=2 ** n)

            # op1 |k> = |K'>
            output1 = input_data.evolve(op1)

            # |K0>
            input_qc2 = ket_zero.tensor(input_data)

            # op2 |K0> = |K'0>
            output2 = input_qc2.evolve(op2)

            # |K'> \otimes |0> = |K'0>
            expected_output = ket_zero.tensor(output1)

            self.assertTrue(output2.equiv(expected_output))




