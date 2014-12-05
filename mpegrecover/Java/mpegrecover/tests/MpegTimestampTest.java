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


package mpegrecover.tests;

import java.lang.Exception;
import java.lang.Math;
import mpegrecover.mpeg.MpegTimestamp;


class MpegTimestampTestable extends MpegTimestamp {
	public char getPosition(int index) {
		return this.storage[index];
	}

	public void setPosition(int index, char value) {
		this.storage[index] = value;
	}

	public void setValueFromInt(int value) {
		for (int i = 0; i < 5; i++)
			this.storage[i] = 0;

		while (value != 0) {
			int index = (int)(Math.log(value) / Math.log(256));
			this.storage[4-index]++;
			value -= Math.pow(256, index);
		}
	}
}

public class MpegTimestampTest {
	public static boolean checkCharArray(MpegTimestampTestable t,
	                                     char[] array) {
		for (int i = 0; i < 5; i++) {
			if (t.getPosition(i) != array[i])
				return false;
		}
		return true;
	}

	public static void testIntValue() throws Exception {
		char[] expected = {0, 7, 0, 52, 52};

		MpegTimestampTestable t = new MpegTimestampTestable();

		t.setValueFromInt(117453876);

		if (! MpegTimestampTest.checkCharArray(t, expected))
			throw new Exception("MpegTimestampTest.checkCharArray(...) " +
			                    "failed.");
	}

	public static void run() throws Exception {
		MpegTimestampTest.testIntValue();
	}
}
