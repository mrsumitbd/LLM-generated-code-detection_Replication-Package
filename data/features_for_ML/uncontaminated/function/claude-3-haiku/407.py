import os
import subprocess

def run_dbCAN_hmmer(config):
    """
    Runs the dbCAN-HMMer pipeline on the input data.

    Args:
        config (dict): A dictionary containing the necessary configuration parameters.

    Returns:
        str: The path to the output directory.
    """
    # Extract the necessary configuration parameters
    input_file = config['input_file']
    output_dir = config['output_dir']
    hmmer_path = config['hmmer_path']
    dbcan_path = config['dbcan_path']

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Run the dbCAN-HMMer pipeline
    subprocess.run([
        hmmer_path, '--cpu', '4', '--domtblout',
        os.path.join(output_dir, 'dbCAN_hmmer_output.txt'),
        os.path.join(dbcan_path, 'dbCAN-HMMer/hmms/dbCAN-HMMer-db.hmm'),
        input_file
    ], check=True)

    return output_dir