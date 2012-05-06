using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public class Level
	{
		public string Name { get; private set; }
		public List<Tile>[] Grid { get; private set; }
		public int Width { get; private set; }
		public int Height { get; private set; }
		private Dictionary<string, string> values = new Dictionary<string, string>();

		public bool IsDirty { get; set; }

		public Level(string name, bool overwrite)
		{
			this.Name = name;
			this.IsDirty = false;
			string filepath = "data/levels/" + name + ".txt";
			if (overwrite && FileStuff.Exists(filepath))
			{
				System.Windows.MessageBox.Show("Warning: a level with this name already exists. Saving this level will overwrite that level.");
			}

			string contents = overwrite ? "" : FileStuff.ReadFile(filepath);
			foreach (string line in contents.Split('\n'))
			{
				string formattedLine = line.Trim();
				if (formattedLine.Length > 0 && formattedLine[0] == '#')
				{
					string[] parts = formattedLine.Substring(1).Split(':');
					if (parts.Length > 1)
					{
						string key = parts[0];
						string value = parts[1];
						for (int i = 2; i < parts.Length; ++i)
						{
							value += ":" + parts[i];
						}
						this.values[key] = value;
					}
				}
			}

			int width = 12;
			int height = 12;
			bool loadTiles =
				this.values.ContainsKey("width") &&
				this.values.ContainsKey("height") &&
				int.TryParse(this.values["width"], out width) &&
				int.TryParse(this.values["height"], out height) &&
				this.values.ContainsKey("tiles");

			this.Width = width;
			this.Height = height;

			this.Grid = new List<Tile>[width * height];
			if (loadTiles)
			{
				string[] rawTileColumns = this.values["tiles"].Split(',');
				
				for (int i = 0; i < width * height; ++i)
				{
					List<Tile> tileStack = new List<Tile>();
					string[] rawTileColumn = rawTileColumns[i].Split('|');
					if (rawTileColumn.Length > 0 && rawTileColumn[0].Length > 0)
					{
						foreach (string rawTileCell in rawTileColumn)
						{
							tileStack.Add(TileStore.GetTile(rawTileCell));
						}
					}
					this.Grid[i] = tileStack;
				}
			}
			else
			{
				for (int i = 0; i < width * height; ++i)
				{
					this.Grid[i] = new List<Tile>();
				}
			}
		}

		public void Resize(string anchor, int width, int height)
		{
			if (width == this.Width && height == this.Height) return;

			List<Tile>[] newGrid = new List<Tile>[width * height];

			// blit old Grid onto newGrid at xOffset, yOffset
			int xOffset = 0;
			int yOffset = 0;
			if (anchor == "left" || anchor == "bottom")
			{
				yOffset = height - this.Height;
			}
			if (anchor == "bottom" || anchor == "right")
			{
				xOffset = width - this.Width;
			}

			int targetX, targetY;
			for (int y = 0; y < this.Height; ++y)
			{
				for (int x = 0; x < this.Width; ++x)
				{
					targetX = x + xOffset;
					targetY = y + yOffset;
					if (targetX >= 0 && targetX < width && targetY >= 0 && targetY < height)
					{
						newGrid[targetX + targetY * width] = this.Grid[x + y * this.Width];
					}
				}
			}


			for (int y = 0; y < height; ++y)
			{
				for (int x = 0; x < width; ++x)
				{
					if (newGrid[x + y * width] == null)
					{
						newGrid[x + y * width] = new List<Tile>();
					}
				}
			}

			this.Width = width;
			this.Height = height;
			this.Grid = newGrid;
			this.IsDirty = true;
		}

		/// <summary>
		/// passing in null tileswatch is an eraser
		/// </summary>
		/// <returns>true if a change has occurred and the view ought to be updated</returns>
		public bool ModifyTile(int col, int row, int layer, Tile tileSwatch)
		{
			if (col < 0 || col >= this.Width || row < 0 || row >= this.Height) return false;
			int index = col + row * this.Width;
			List<Tile> tileStack = this.Grid[index];
			List<Tile> spread = new List<Tile>();
			foreach (Tile tile in tileStack)
			{
				if (tile == null)
				{
					spread.Add(null);
				}
				else
				{
					spread.Add(tile);
					for (int i = 1; i < tile.Height; ++i)
					{
						spread.Add(null);
					}
				}
			}

			while (spread.Count <= layer)
			{
				spread.Add(null);
			}

			spread[layer] = tileSwatch;
			List<Tile> output = new List<Tile>();
			for (int i = 0; i < spread.Count; ++i)
			{
				output.Add(spread[i]);
				if (spread[i] != null)
				{
					i += spread[i].Height - 1;
				}
			}

			if (output.Count != tileStack.Count)
			{
				tileStack.Clear();
				tileStack.AddRange(output);
				return true;
			}
			bool changes = false;
			for (int i = 0; i < output.Count; ++i)
			{
				if (output[i] != tileStack[i])
				{
					tileStack[i] = output[i];
					changes = true;
				}
			}

			return changes;
		}

		public void Save()
		{
			Dictionary<string, string> outputValues = new Dictionary<string, string>(this.values);
			outputValues["width"] = this.Width.ToString();
			outputValues["height"] = this.Height.ToString();
			List<string> tiles = new List<string>();
			foreach (List<Tile> tileStack in this.Grid)
			{
				string value = tileStack.Count == 0 ? "" : string.Join("|", tileStack.Select<Tile, string>(tile => tile == null ? "0" : tile.ID));
				while (value.EndsWith("|0"))
				{
					value = value.Substring(0, value.Length - 2);
				}
				tiles.Add(value);
			}
			outputValues["tiles"] = string.Join(",", tiles);

			List<string> output = new List<string>();
			foreach (string key in outputValues.Keys)
			{
				output.Add("#" + key + ":" + outputValues[key]);
			}
			string finalOutput = string.Join("\r\n", output);
			FileStuff.WriteFile("data/levels/" + this.Name + ".txt", finalOutput);
			this.IsDirty = false;
		}
	}
}
