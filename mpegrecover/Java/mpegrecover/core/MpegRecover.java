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


package mpegrecover.core;

import mpegrecover.configuration.Configuration;


public class MpegRecover {
	private Configuration conf;

	public static void main(String[] args) {
		new MpegRecover(args).run();
	}

	public MpegRecover(String[] args) {
		this.conf = new Configuration();
		this.conf.parseCmdLineArgs(args);
	}

	public void dumpConfiguration() {
		System.out.println("Configuration:");

		System.out.print(" Verbose:      ");
		System.out.println(new Boolean(conf.getVerbose()).toString());

		System.out.print(" Blocksize:    ");
		System.out.println(new Integer(conf.getBlocksize()).toString());

		System.out.print(" Gapsize:      ");
		System.out.println(new Integer(conf.getGapsize()).toString());

		System.out.print(" Discardsize:  ");
		System.out.println(new Integer(conf.getDiscardsize()).toString());

		System.out.print(" Inputfile:    ");
		System.out.println(conf.getInput());

		System.out.print(" Outputdir:    ");
		System.out.println(conf.getOutput());

		System.out.println();
	}

	public void run() {
		if (this.conf.getVerbose()) {
			this.dumpConfiguration();
		}

		this.usage();
	}

	public void usage() {
		System.out.println(
			"Syntax: java -jar mpegrecover.jar [options] input-filename output-directory\n" +
			"Options:\n" +
			"  -b N        set block-size\n" +
			"  -g N        set gap-size\n" +
			"  -d N        set discard-size\n" +
			"  -v          enable verbose mode\n" +
			"  -h          display this message"
		);
	}
}
