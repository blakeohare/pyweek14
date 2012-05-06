using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public static class Model
	{
		static Model()
		{
			IsHiddenLayersVisible = true;
		}

		public static Level ActiveLevel
		{
			get;
			set;
		}

		public static Tile ActiveTileSwatch
		{
			get;
			set;
		}

		public static int LayerCutoff
		{
			get { return MainWindow.LayerCutoff; }
		}

		public static bool IsHiddenLayersVisible
		{
			get;
			set;
		}
	}
}
