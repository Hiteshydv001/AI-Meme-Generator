# main.py

import argparse
import trainer
import tester

def main():
    """Main entry point for the Meme Bot AI application."""
    parser = argparse.ArgumentParser(
        description="Train and test a Reinforcement Learning agent to be funny.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "mode",
        choices=['train', 'test'],
        help="""Choose the mode to run:
  'train' - Start or continue training the AI model.
  'test'  - Test the latest trained model to see how funny it is."""
    )

    args = parser.parse_args()

    if args.mode == 'train':
        trainer.train_agent()
    elif args.mode == 'test':
        tester.test_agent()

if __name__ == "__main__":
    main()