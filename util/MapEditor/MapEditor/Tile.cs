using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MapEditor
{
	public class Tile
	{
		private System.Windows.Media.ImageSource imageSource = null;

		public string ID { get; set; }
		public string Category { get; set; }
		public int Height { get; set; }
		public string[] ImageFiles { get; set; }
		public System.Windows.Media.ImageSource Image
		{
			get
			{
				if (this.imageSource == null &&
					this.ImageFiles != null &&
					this.ImageFiles.Length > 0)
				{
					string path = this.ImageFiles[0];
					this.imageSource = new System.Windows.Media.Imaging.BitmapImage(
						new Uri(FileStuff.CanonicalizePath(path), UriKind.Absolute));
				}
				return this.imageSource;
			}
		}
	}
}
