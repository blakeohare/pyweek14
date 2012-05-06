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

		public Level(string name, bool overwrite)
		{
			this.Name = name;

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

		public void Save()
		{
			Dictionary<string, string> outputValues = new Dictionary<string, string>(this.values);
			outputValues["width"] = this.Width.ToString();
			outputValues["height"] = this.Height.ToString();
			List<string> tiles = new List<string>();
			foreach (List<Tile> tileStack in this.Grid)
			{
				tiles.Add(tileStack.Count == 0 ? "" : string.Join("|", tileStack.Select<Tile, string>(tile => tile.ID)));
			}
			outputValues["tiles"] = string.Join(",", tiles);

			List<string> output = new List<string>();
			foreach (string key in outputValues.Keys)
			{
				output.Add("#" + key + ":" + outputValues[key]);
			}
			string finalOutput = string.Join("\r\n", output);
			FileStuff.WriteFile("data/levels/" + this.Name + ".txt", finalOutput);
		}
	}
}
