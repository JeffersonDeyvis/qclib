#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Test qclib.gate.log_mcx_gate """

from unittest import TestCase
from qiskit.quantum_info import Operator
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

    @staticmethod
    def reduzir_matriz(U, num_qubits, qubit_aux=3):
        """Reduz a matriz unitária ao subespaço onde o último qubit está em |0>."""
        n = 2 ** num_qubits
        indices = [i for i in range(n) if (i & (1 << qubit_aux)) == 0]
        return U[np.ix_(indices, indices)]


    # def test_circuit_one_clean_ancilla(self):
    #     n_controls = 9
    #     target = [0]
    #     qc1 = LogMcx.circuit_one_clean_ancilla(n_controls) # mcx, 11 qubits sendo o ultimo clean ancila
    #     qc2 = QuantumCircuit(n_controls+1) # 10 qubits
    #     qc2.mcx(list(range(1, n_controls+1)), target)  # mcx com 9 controles
    #
    #
    #     u2 = Operator(qc2)
    #     projector_ancilla = Operator([[1, 0], [0, 0]])
    #     expected_u2 = u2.tensor(projector_ancilla)
    #
    #     u1 = Operator(qc1).data
    #     identity = np.eye(2 ** (n_controls + 1))
    #     total_projector = np.kron(identity, projector_ancilla)
    #
    #     projected_op = total_projector @ u1
    #
    #     self.assertTrue(np.allclose(projected_op, expected_u2.data))



