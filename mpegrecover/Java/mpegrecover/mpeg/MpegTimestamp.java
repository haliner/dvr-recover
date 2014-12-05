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


package mpegrecover.mpeg;

/**
 * MpegTimestamp saves a single timestamp which is used in MPEG streams.
 */
public class MpegTimestamp {
	/**
	 * A char array used for storage.
	 *
	 * Each char can hold exactly one byte, which holds 8 bit. The timestamp
	 * of an MPEG block is saved in 33 bits. That's why we need 5 bytes and
	 * only 1 bit is used in the last one.
	 *
	 * The timestamp's value is stored in big endian format.
	 */
	protected char[] storage;

	/* Constructor */

	/**
	 * Creates new MpegTimestamp which value is 0.
	 */
	public MpegTimestamp() {
		this.storage = new char[5];
	}

	/**
	 * Copys another MpegTimestamp object.
	 */
	public MpegTimestamp(MpegTimestamp time) {
		this();

		for (int i = 0; i < 5; i++) {
			this.storage[i] = time.storage[i];
		}
	}

	/* Static functions */

	/**
	 * Compares object with another MpegTimestamp object.
	 *
	 * @return True if both object's values are equal. Otherwise False.
	 */
	public boolean isEqual(MpegTimestamp time) {
		for (int i = 0; i < 5; i++)
			if (this.storage[i] != time.storage[i])
				return false;
		return true;
	}

	/**
	 * Compares object with another MpegTimestamp object.
	 *
	 * @return True if this object's value is bigger.
	 */
	public boolean isBigger(MpegTimestamp time) {
		for (int i = 0; i < 5; i++) {
			if (this.storage[i] == time.storage[i])
				continue;
			else
				return (this.storage[i] > time.storage[i]);
		}
		return false;
	}

	/**
	 * Compares object with another MpegTimestamp object.
	 *
	 * @return True if this object's value is smaller.
	 */
	public boolean isSmaller(MpegTimestamp time) {
		for (int i = 0; i < 5; i++)
			if (this.storage[i] == time.storage[i])
				continue;
			else
				return (this.storage[i] < time.storage[i]);
		return false;
	}

	/**
	 * Calculates the difference between two MpegTimestamp.
	 *
	 * Note that a MpegTimestamp can only hold positive values. The difference
	 * has also always a positive value.
	 *
	 * @return The difference as new MpegTimestamp object.
	 */
	public static MpegTimestamp difference(MpegTimestamp t1, MpegTimestamp t2) {
		/*
		 * Which timestamp is the bigger one? We subtract the smaller from
		 * the bigger one, to get a correct and positive result.
		 */
		MpegTimestamp big, small;
		if (t1.isBigger(t2)) {
			big = t1;
			small = t2;
		} else {
			big = t2;
			small = t1;
		}

		MpegTimestamp result = new MpegTimestamp();
		for (int i = 4; i >= 0; i--) {
			/*
			 * Calculate the difference of each positions separately.
			 */
			result.storage[i] += big.storage[i] - small.storage[i];
			if (big.storage[i] < small.storage[i]) {
				/*
				 * If the difference is negative, decrement the next position
				 * (the one with the higher significance). For a negative
				 * difference a arithmetic overflow occurs -- exactly what's
				 * needed.
				 *
				 * If the next position in big is a zero, the decrementation
				 * will overflow, too. For a correct result, we must decrement
				 * the next position again and so on.
				*/
				for (int j = i-1; j >= 0; j--) {
					result.storage[j]--;
					if (big.storage[j] != 0)
						break;
				}
			}
		}

		return result;
	}
}
