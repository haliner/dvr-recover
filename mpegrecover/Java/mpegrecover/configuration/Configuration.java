/*
 * Copyright (C) 2010  Stefan Haller <haliner@googlemail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


package mpegrecover.configuration;


public class Configuration {
	protected boolean verbose;
	protected int blocksize;
	protected int gapsize;
	protected int discardsize;
	protected boolean help;
	protected String input;
	protected String output;



	/* Constructor */

	public Configuration() {
		this.reset();
	}



	/* Properties */

	public boolean getVerbose() {
		return this.verbose;
	}

	public void setVerbose(boolean value) {
		this.verbose = value;
	}


	public int getBlocksize() {
		return this.blocksize;
	}

	public void setBlocksize(int value) {
		this.blocksize = value;
	}


	public int getGapsize() {
		return this.gapsize;
	}

	public void setGapsize(int value) {
		this.gapsize = value;
	}


	public int getDiscardsize() {
		return this.discardsize;
	}

	public void setDiscardsize(int value) {
		this.discardsize = value;
	}


	public boolean getHelp() {
		return this.help;
	}

	public void setHelp(boolean value) {
		this.help = value;
	}


	public String getInput() {
		return this.input;
	}

	public void setInput(String value) {
		this.input = value;
	}


	public String getOutput() {
		return this.output;
	}

	public void setOutput(String value) {
		this.output = value;
	}



	/* Other functions */

	/**
	 * Checks if all necessary options are set.
	 *
	 * @return true if all necessary options are set, otherwise false
	 */
	public boolean check() {
		return ((this.getInput() != null) &&
		        (this.getOutput() != null));
	}

	/**
	 * Parses command line arguments and sets properties accordingly.
	 *
	 * @param args the command line arguments
	 */
	public void parseCmdLineArgs(String[] args) {
		/*
		 * TODO: Implement better command line argument parsing!
		 */


		int i;
		for (i = 0; i < args.length; i++) {
			String arg_current = args[i];
			String arg_next = null;
			if (i != args.length - 1)
				arg_next = args[i + 1];

			if (arg_current.equals("-v"))
				this.setVerbose(true);
			else
			if (arg_current.equals("-b"))
				this.setBlocksize(Integer.parseInt(arg_next));
			else
			if (arg_current.equals("-g"))
				this.setGapsize(Integer.parseInt(arg_next));
			else
			if (arg_current.equals("-d"))
				this.setDiscardsize(Integer.parseInt(arg_next));
			else
				break;
		}

		/* TODO: Better checking for parameter count. */
		if (args.length - i == 2) {
			this.setInput(args[i]);
			this.setOutput(args[i + 1]);
		}
	}

	/**
	 * Reset configuration to default values.
	 *
	 * The following default settings are applied: <br><br>
	 * Verbose = False <br>
	 * Blocksize = 2048 <br>
	 * Gapsize = 90.000 (= 1 second) <br>
	 * Discardsize = 27.000.000 (= 5 minutes)
	 */
	public void reset() {
		this.verbose = false;
		this.blocksize = 2048;
		this.gapsize = 90000;
		this.discardsize = 27000000;
		this.input = null;
		this.output = null;
	}
}
