from qsurface.codes.elements import AncillaQubit
from ..toric.sim import PerfectMeasurements as ToricPM, FaultyMeasurements as ToricFM


class PerfectMeasurements(ToricPM):
    # Inherited docstring

    name = "planar"

    def init_surface(self, z: float = 0, **kwargs):
        """Initializes the linear code on layer ``z``.

        Parameters
        ----------
        z : int or float, optional
            Layer of qubits, ``z=0`` for perfect measurements.
        """
        self.ancilla_qubits[z], self.data_qubits[z], self.pseudo_qubits[z] = {}, {}, {}
        parity = self.init_parity_check

        # Add data qubits to surface
        for x in range(self.size[0]):
            self.add_data_qubit((x, 0), z=z, **kwargs)

        # Add ancilla qubits to surface
        for x in range(self.size[0]-1):
            parity(self.add_ancilla_qubit((x+0.5, 0), z=z, state_type="x", **kwargs))

        parity(self.add_pseudo_qubit((-0.5, 0), z=z, state_type="x", **kwargs))
        parity(self.add_pseudo_qubit((self.size[0]-0.5, 0), z=z, state_type="x", **kwargs))

    def init_parity_check(self, ancilla_qubit: AncillaQubit, **kwargs):
        """Initiates a parity check measurement.

        For every ancilla qubit on ``(x,y)``, four neighboring data qubits are entangled for parity check measurements.

        Parameters
        ----------
        ancilla_qubit : `~.codes.elements.AncillaQubit`
            Ancilla qubit to initialize.
        """
        (x, y), z = ancilla_qubit.loc, ancilla_qubit.z
        checks = {
            (0.5, 0): ((x + 0.5), y),
            (-0.5, 0): ((x - 0.5), y),
        }
        for key, loc in checks.items():
            if loc in self.data_qubits[z]:
                self.entangle_pair(self.data_qubits[z][loc], ancilla_qubit, key)

    def init_logical_operator(self, **kwargs):
        """Initiates the logical operators [x,z] of the planar code."""
        operators = {
            "x": [self.data_qubits[self.decode_layer][(self.size[0]-1, 0)].edges["x"]],
        }
        self.logical_operators = operators


class FaultyMeasurements(ToricFM, PerfectMeasurements):
    # Inherited docstring

    pass
