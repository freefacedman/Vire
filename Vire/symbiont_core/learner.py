import pathlib

class Learner:
    """Symbiont's learning module: loads and digests inputs."""

    def __init__(self, inputs_path=None):
        if inputs_path:
            self.inputs_path = pathlib.Path(inputs_path)
        else:
            self.inputs_path = pathlib.Path(__file__).resolve().parents[1] / 'memory' / 'inputs'

    def list_inputs(self):
        """List all available learning files."""
        return list(self.inputs_path.glob('*.txt'))

    def load_input(self, filename):
        """Load a specific input file as text."""
        file_path = self.inputs_path / filename
        if file_path.exists():
            try:
                text = file_path.read_text(encoding='utf-8')
                if not text.strip():
                    print(f"⚠️ Warning: {filename} is empty or unreadable.")
                    return None
                return text
            except Exception as e:
                print(f"❌ Failed reading {filename}: {e}")
                return None
        else:
            print(f"❌ File {filename} does not exist.")
            return None

    def summarize(self, text):
        """Basic digest: summarize the input to main ideas."""
        if not text:
            print(f"⚠️ Empty text received for summarization.")
            return []

        lines = text.splitlines()
        # Allow shorter lines (drop strict >30 rule)
        keypoints = [line.strip() for line in lines if line.strip()]

        if not keypoints:
            print(f"⚠️ No usable content found after cleaning lines.")
            return []

        return keypoints[:5]  # crude first digest: top 5 lines
