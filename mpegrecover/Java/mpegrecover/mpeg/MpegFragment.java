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
 * This class represents a continious stream of MPEG data in a larger block
 * of data.
 *
 * Generally you can see an MPEG fragment as a concatenation of multiple
 * MPEG blocks.
 */
public class MpegFragment {
	private int start;
	private int size;
	private MpegTimestamp startTime;
	private MpegTimestamp endTime;

	/* Properties */

	public int getStart() {
		return this.start;
	}

	public void setStart(int value) {
		this.start = value;
	}

	public int getEnd() {
		return this.getStart() + this.getSize();
	}

	public void setEnd(int value) {
		this.size = value - this.getStart();
	}

	public int getSize() {
		return this.size;
	}

	public void setSize(int value) {
		this.size = value;
	}

	public MpegTimestamp getStartTime() {
		return this.startTime;
	}

	public void setStartTime(MpegTimestamp value) {
		this.startTime = value;
	}

	public MpegTimestamp getEndTime() {
		return this.endTime;
	}

	public void setEndTime(MpegTimestamp value) {
		this.endTime = value;
	}

	/* Other functions */

	public MpegTimestamp getTimeDiff() {
		return MpegTimestamp.difference(this.getEndTime(), this.getStartTime());
	}
}
