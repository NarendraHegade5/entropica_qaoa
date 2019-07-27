import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import numpy as np
from pytest import raises

from pyquil.paulis import PauliSum, PauliTerm
from pyquil.quil import QubitPlaceholder, Qubit

from entropica_qaoa.qaoa.parameters import (ExtendedParams,
                                         StandardWithBiasParams,
                                         AnnealingParams,
                                         FourierParams,
                                         FourierWithBiasParams,
                                         QAOAParameterIterator,
                                         AbstractParams,
                                         StandardParams)

# build a hamiltonian to test everything on
q1 = QubitPlaceholder()
# hamiltonian = PauliSum.from_compact_str("1.0*Z0Z1")
hamiltonian = PauliTerm("Z", 0)
hamiltonian *= PauliTerm("Z", 1)
hamiltonian += PauliTerm("Z", q1, 0.5)
next_term = PauliTerm("Z", 0, -2.0)
next_term *= PauliTerm("Z", q1)
hamiltonian += next_term

# TODO Test plot functionality
# TODO test fourier params
# TODO Test set_hyperparameters and update_variable_parameters
def test_ExtendedParams():
    params = ExtendedParams.linear_ramp_from_hamiltonian(hamiltonian, 2, time=2)
    assert set(params.reg) == {0, 1, q1}
    assert np.allclose(params.betas, [[0.75] * 3, [0.25] * 3])
    assert np.allclose(params.gammas_singles, [[0.25], [0.75]])
    assert np.allclose(params.gammas_pairs, [[0.25, 0.25], [0.75, 0.75]])
    assert [params.qubits_singles] == [term.get_qubits() for term in hamiltonian
                                       if len(term) == 1]
    # Test updating and raw output
    raw = np.random.rand(len(params))
    params.update_from_raw(raw)
    assert np.allclose(raw, params.raw())

# TODO check that the values also make sense
def test_ExtendedParamsfromAbstractParameters():
    abstract_params = AbstractParams((hamiltonian, 2))
    betas          = [[0.0, 0.1, 0.3], [0.5, 0.2, 1.2]]
    gammas_singles = [[0.0], [0.5]]
    gammas_pairs   = [[0.1, 0.3], [0.2, 1.2]]
    parameters = (betas, gammas_singles, gammas_pairs)
    general_params = ExtendedParams.from_AbstractParameters(abstract_params, parameters)
    print("The rotation angles from ExtendedParams.fromAbstractParameters")
    print("x_rotation_angles:\n", general_params.x_rotation_angles)
    print("z_rotation_angles:\n", general_params.z_rotation_angles)
    print("zz_rotation_angles:\n", general_params.zz_rotation_angles)

# Todo: Check that the values also make sense
def test_StandardWithBiasParamsfromAbstractParameters():
    abstract_params = AbstractParams((hamiltonian, 2))
    betas          = [np.pi, 0.4]
    gammas_singles = [10, 24]
    gammas_pairs   = [8.8, 2.3]
    parameters = (betas, gammas_singles, gammas_pairs)
    alternating_params = StandardWithBiasParams.from_AbstractParameters(abstract_params, parameters)
    print("The rotation angles from StandardWithBiasParams.fromAbstractParameters")
    print("x_rotation_angles:\n", alternating_params.x_rotation_angles)
    print("z_rotation_angles:\n", alternating_params.z_rotation_angles)
    print("zz_rotation_angles:\n", alternating_params.zz_rotation_angles)
    assert type(alternating_params) == StandardWithBiasParams


# Todo: Check that the values also make sense
def test_AnnealingParamsfromAbstractParameters():
    abstract_params = AbstractParams((hamiltonian, 2))
    schedule = [0.4, 1.0]
    parameters = (schedule)
    adiabatic_params = AnnealingParams.from_AbstractParameters(abstract_params, parameters, time=5.0)
    print("The rotation angles from AnnealingParams.fromAbstractParameters")
    print("x_rotation_angles:\n", adiabatic_params.x_rotation_angles)
    print("z_rotation_angles:\n", adiabatic_params.z_rotation_angles)
    print("zz_rotation_angles:\n", adiabatic_params.zz_rotation_angles)
    assert type(adiabatic_params) == AnnealingParams


# Todo: Check that the values also make sense
def test_FourierParamsfromAbstractParameters():
    abstract_params = AbstractParams((hamiltonian, 2))
    v = [0.4, 1.0]
    u_singles = [0.5, 1.2]
    u_pairs = [4.5, 123]
    parameters = (v, u_singles, u_pairs)
    fourier_params = FourierParams.from_AbstractParameters(abstract_params, parameters, q=2)
    print("The rotation angles from AnnealingParams.fromAbstractParameters")
    print("x_rotation_angles:\n", fourier_params.x_rotation_angles)
    print("z_rotation_angles:\n", fourier_params.z_rotation_angles)
    print("zz_rotation_angles:\n", fourier_params.zz_rotation_angles)
    assert type(fourier_params) == FourierParams


def test_AnnealingParams():
    params = AnnealingParams.linear_ramp_from_hamiltonian(hamiltonian, 2, time=2)
    assert set(params.reg) == {0, 1, q1}
    assert np.allclose(params.x_rotation_angles, [[0.75] * 3, [0.25] * 3])
    assert np.allclose(params.z_rotation_angles, [[0.125], [0.375]])
    assert np.allclose(params.zz_rotation_angles, [[0.25, -0.5], [0.75, -1.5]])
    assert [params.qubits_singles] == [term.get_qubits() for term in hamiltonian
                                       if len(term) == 1]
    # Test updating and raw output
    raw = np.random.rand(len(params))
    params.update_from_raw(raw)
    assert np.allclose(raw, params.raw())


def test_StandardWithBiasParams():
    params = StandardWithBiasParams.linear_ramp_from_hamiltonian(hamiltonian, 2, time=2)
    assert set(params.reg) == {0, 1, q1}
    assert np.allclose(params.x_rotation_angles, [[0.75] * 3, [0.25] * 3])
    assert np.allclose(params.z_rotation_angles, [[0.125], [0.375]])
    assert np.allclose(params.zz_rotation_angles, [[0.25, -0.5], [0.75, -1.5]])
    assert [params.qubits_singles] == [term.get_qubits() for term in hamiltonian
                                       if len(term) == 1]
    # Test updating and raw output
    raw = np.random.rand(len(params))
    params.update_from_raw(raw)
    assert np.allclose(raw, params.raw())

def test_StandardParams():
    params = StandardParams.linear_ramp_from_hamiltonian(hamiltonian, 2, time=2)
    assert set(params.reg) == {0, 1, q1}
    assert np.allclose(params.x_rotation_angles, [[0.75] * 3, [0.25] * 3])
    assert np.allclose(params.z_rotation_angles, [[0.125], [0.375]])
    assert np.allclose(params.zz_rotation_angles, [[0.25, -0.5], [0.75, -1.5]])
    assert [params.qubits_singles] == [term.get_qubits() for term in hamiltonian
                                       if len(term) == 1]
    # Test updating and raw output
    raw = np.random.rand(len(params))
    params.update_from_raw(raw)
    assert np.allclose(raw, params.raw())


def test_non_fourier_params_are_consistent():
    """
    Check that StandardParams, StandardWithBiasParams and
    ExtendedParams give the same rotation angles, given the same data"""
    p1 = StandardParams.linear_ramp_from_hamiltonian(hamiltonian, 2, time=2)
    p2 = ExtendedParams.linear_ramp_from_hamiltonian(hamiltonian, 2, time=2)
    p3 = StandardWithBiasParams.linear_ramp_from_hamiltonian(hamiltonian,
                                                             2, time=2)
    assert np.allclose(p1.x_rotation_angles, p2.x_rotation_angles)
    assert np.allclose(p2.x_rotation_angles, p3.x_rotation_angles)
    assert np.allclose(p1.z_rotation_angles, p2.z_rotation_angles)
    assert np.allclose(p2.z_rotation_angles, p3.z_rotation_angles)
    assert np.allclose(p1.zz_rotation_angles, p2.zz_rotation_angles)
    assert np.allclose(p2.zz_rotation_angles, p3.zz_rotation_angles)


def test_FourierParams():
    params = FourierParams.linear_ramp_from_hamiltonian(hamiltonian, n_steps=3, q=2, time=2)
    # just access the angles, to check that it actually creates them
    assert len(params.z_rotation_angles) == len(params.zz_rotation_angles)
    assert np.allclose(params.v, [2/3, 0])
    assert np.allclose(params.u, [2/3, 0])
    # Test updating and raw output
    raw = np.random.rand(len(params))
    params.update_from_raw(raw)
    assert np.allclose(raw, params.raw())


def test_FourierWithBiasParams():
    params = FourierWithBiasParams.linear_ramp_from_hamiltonian(hamiltonian, n_steps=3, q=2, time=2)
    # just access the angles, to check that it actually creates them
    assert len(params.z_rotation_angles) == len(params.zz_rotation_angles)
    assert np.allclose(params.v, [2/3, 0])
    assert np.allclose(params.u_singles, [2/3, 0])
    assert np.allclose(params.u_pairs, [2/3, 0])
    # Test updating and raw output
    raw = np.random.rand(len(params))
    params.update_from_raw(raw)
    assert np.allclose(raw, params.raw())


def test_FourierParams_are_consistent():
    """
    Check, that both Fourier Parametrizations give the same rotation angles,
    given the same data"""
    params1 = FourierParams.linear_ramp_from_hamiltonian(
                  hamiltonian, n_steps=3, q=2, time=2)
    params2 = FourierWithBiasParams.linear_ramp_from_hamiltonian(
                  hamiltonian, n_steps=3, q=2, time=2)

    assert np.allclose(params1.x_rotation_angles, params2.x_rotation_angles)
    assert np.allclose(params1.z_rotation_angles, params2.z_rotation_angles)
    assert np.allclose(params1.zz_rotation_angles, params2.zz_rotation_angles)


def test_QAOAParameterIterator():
    params = AnnealingParams.linear_ramp_from_hamiltonian(hamiltonian, 2)
    iterator = QAOAParameterIterator(params, "schedule[0]", np.arange(0,1,0.5))
    log = []
    for p in iterator:
        log.append((p.schedule).copy())
    print(log[0])
    print(log[1])
    assert np.allclose(log[0], [0, 0.75])
    assert np.allclose(log[1], [0.5, 0.75])


def test_inputChecking():
    # ham = PauliSum.from_compact_str("0.7*Z0*Z1")
    ham = PauliSum([PauliTerm("Z", 0, 0.7) * PauliTerm("Z", 1)])
    betas = [1, 2, 3, 4]
    gammas_singles = []
    gammas_pairs = [1, 2, 3]
    with raises(ValueError):
        params = ExtendedParams((ham, 3),
                                (betas, gammas_singles, gammas_pairs))
