#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Test qclib.gate.log_mcx_gate """

from unittest import TestCase

import numpy as np
# from scipy.stats import unitary_group
import qiskit
from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library import MCXGate
import qclib.util
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


