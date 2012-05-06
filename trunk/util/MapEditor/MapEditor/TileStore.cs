using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public static class TileStore
	{
		private static Dictionary<string, Tile> tilesById = new Dictionary<string, Tile>();
		private static Dictionary<string, Dictionary<string, Tile>> tilesByCategory = new Dictionary<string, Dictionary<string, Tile>>();
		public static void Initialize()
		{
			string folder = "data/tile_manifests";
			string[] files = FileStuff.GetFilesInFolder(folder, false);
			foreach (string file in files)
			{
				string path = folder + "/" + file;
				string contents = FileStuff.ReadFile(path);
				string name = file.EndsWith(".txt") ? file.Substring(0, file.Length - 4) : file;

				InitializeCategory(name, contents);
			}
		}

		public static string[] GetSortedCategories()
		{
			return tilesByCategory.Keys.ToArray<string>();
		}

		public static Tile[] GetSortedTilesForCategory(string category)
		{
			return tilesByCategory[category].Values
				.OrderBy<Tile, string>(tile => tile.ImageFiles[0])
				.ToArray<Tile>();
		}

		private static void InitializeCategory(string categoryName, string fileContents)
		{
			foreach (string[] columns in SanitzeLines(fileContents))
			{
				Tile t = CreateTile(categoryName, columns);
				if (t != null)
				{
					if (tilesById.ContainsKey(t.ID))
					{
						System.Windows.MessageBox.Show("Duplicate tile ID! " + t.ID + " is in " + categoryName + " and " + tilesById[t.ID].Category);
					}
					else
					{
						tilesById.Add(t.ID, t);
						Dictionary<string, Tile> d;
						if (!tilesByCategory.TryGetValue(categoryName, out d))
						{
							d = new Dictionary<string, Tile>();
							tilesByCategory[categoryName] = d;
						}

						d[t.ID] = t;
					}
				}
				else
				{
					System.Windows.MessageBox.Show("Syntax error in " + categoryName);
				}
			}
		}

		private static Tile CreateTile(string category, string[] columns)
		{
			Tile t = new Tile()
			{
				ID = columns[0],
				Category = category
			};

			string[] images = columns[1].Split('|');
			int anim = 4;
			int i = 0;
			if (int.TryParse(images[0], out anim))
			{
				++i;
			}

			List<string> frames = new List<string>();
			for (; i < images.Length; ++i)
			{
				frames.Add("images/tiles/" + images[i]);
			}

			t.ImageFiles = frames.ToArray();
			return t;
		}

		private static List<string[]> SanitzeLines(string contents)
		{
			List<string[]> lines = new List<string[]>();
			string[] raw_lines = contents.Split('\n');
			foreach (string line in raw_lines)
			{
				if (line.Length > 0)
				{
					if (line[0] != '#')
					{
						string[] columns = line.Split('\t');
						if (columns.Length >= 4)
						{
							for (int i = 0; i < columns.Length; ++i)
							{
								columns[i] = columns[i].Trim();
							}
							lines.Add(columns);
						}
					}
				}
			}
			return lines;
		}
	}
}
