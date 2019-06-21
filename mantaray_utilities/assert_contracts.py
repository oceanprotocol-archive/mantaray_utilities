
#%% CHECKING CONTRACT VERSIONS!
# Assert versions of contract definitions (ABI files) match your installed keeper-contracts package version.
if 0:
    #TODO: MOVE TO UTILITIES!
    import pip_api
    import json
    version_kc_installed = 'v'+str(pip_api.installed_distributions()['keeper-contracts'].version)
    network_name = 'pacific'
    path_artifacts = Path(ocn._config.keeper_path)
    # path_artifacts = Path.cwd() / folder_artifacts
    assert path_artifacts.exists()
    path_artifacts.glob("*.{}.json".format(network_name))
    for path_artifact_file in path_artifacts.glob("*.{}.json".format(network_name)):
        logging.debug("Checking {}".format(path_artifacts))
        with open(path_artifact_file) as fp:
            artifact_dict = json.load(fp)
            # print(artifact_dict['version'])
        assert artifact_dict['version'] == version_kc_installed, \
            "Artifact version mismatch, ABI files {} != {} specified in environment".format(artifact_dict['version'], version_kc_installed)
    logging.info("Contract ABI {} == installed version {}, confirmed".format(artifact_dict['version'], version_kc_installed))

#%% Assert code at this smart contract address
if 0:
    from squid_py.keeper.web3_provider import Web3Provider
    from squid_py.keeper.web3_provider import Web3Provider
    # ConfigProvider.set_config(configuration)
    this_web3 = Web3Provider.get_web3()
    for path_artifact_file in path_artifacts.glob("*.{}.json".format(network_name)):
        with open(path_artifact_file) as fp:
            artifact_dict = json.load(fp)
            logging.debug("Checking {} at {}".format(artifact_dict['name'],artifact_dict['address']))
        code = this_web3.eth.getCode(artifact_dict['address'])
        assert code, "No code found on-chain for {} at {}".format(path_artifact_file, artifact_dict['address'])
    logging.info("All {} ABI addresses confirmed to exist on-chain.".format(artifact_dict['version']))
