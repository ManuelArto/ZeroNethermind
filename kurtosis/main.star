"""
ZeroNethermind Demo - Kurtosis Package

This package sets up:
1. A zero-prover API service
2. An Ethereum testnet using the ethereum-package with ZeroNethermind EL client configured for ZkValidation.
"""

# Import the ethereum-package for testnet setup
ethereum_package = import_module("github.com/ethpandaops/ethereum-package/main.star")

def run(plan, args={}):
    """
    Main entry point for the ZeroNethermind demo package.
    
    Args:
        plan: Kurtosis plan object
        args: Configuration arguments (merged with defaults)
    """
    
    # Step 1: Start the zero-prover API service
    zero_prover_service = start_zero_prover(plan)
    prover_url = "http://{}:{}".format(
        zero_prover_service.hostname,
        zero_prover_service.ports["http"].number
    )
    
    # Step 2: Run the ethereum-package to start the testnet
    ethereum_package.run(plan, args)
    
    plan.print("=" * 60)
    plan.print("ZeroNethermind Demo Started!")
    plan.print("Zero-Prover API: " + prover_url)
    plan.print("=" * 60)


def start_zero_prover(plan):
    """
    Start the zero-prover mock API service.
    Builds the Docker image from the zero-prover directory and runs it.
    """
    
    zero_prover_service = plan.add_service(
        name="zero-prover",
        config=ServiceConfig(
            image="zero-prover:local",
            ports={
                "http": PortSpec(
                    number=5000,
                    transport_protocol="TCP",
                    application_protocol="http",
                    wait="30s",
                ),
            },
            ready_conditions=ReadyCondition(
                recipe=GetHttpRequestRecipe(
                    port_id="http",
                    endpoint="/health",
                ),
                field="code",
                assertion="==",
                target_value=200,
                timeout="60s",
            ),
        ),
    )
    
    return zero_prover_service
