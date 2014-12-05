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
 * A single MPEG block.
 *
 * Each MPEG block contains MPEG data. Timestamp information belong also to
 * an MPEG block.
 */
public class MpegBlock {
	private int index;
	private MpegTimestamp time;

	/* Constructor */

	public MpegBlock(int index, MpegTimestamp time) {
		this.setIndex(index);
		this.setTime(time);
	}

	/* Properties */

	public int getIndex() {
		return this.index;
	}

	public void setIndex(int value) {
		this.index = value;
	}

	public MpegTimestamp getTime() {
		return this.time;
	}

	public void setTime(MpegTimestamp value) {
		this.time = value;
	}
}
