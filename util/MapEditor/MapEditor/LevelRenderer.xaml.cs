using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace MapEditor
{
	/// <summary>
	/// Interaction logic for LevelRenderer.xaml
	/// </summary>
	public partial class LevelRenderer : UserControl
	{
		private Level level;
		private ImageSource foundationImage;
		public LevelRenderer(Level level)
		{
			this.level = level;
			InitializeComponent();
			this.foundationImage = ((Image)this.Resources["foundation_image"]).Source;
			this.Refresh();
			this.clicker_catcher.MouseMove += new MouseEventHandler(clicker_catcher_MouseMove);
			this.clicker_catcher.MouseDown += new MouseButtonEventHandler(clicker_catcher_MouseDown);
			this.clicker_catcher.MouseUp += new MouseButtonEventHandler(clicker_catcher_MouseUp);
		}

		private bool isDrawing = false;
		private bool isErasing = false;
		void clicker_catcher_MouseUp(object sender, MouseButtonEventArgs e)
		{
			this.isDrawing = false;
			this.last_modified_x = -1;
			this.last_modified_y = -1;
		}

		void clicker_catcher_MouseDown(object sender, MouseButtonEventArgs e)
		{
			this.isDrawing = true;
			this.isErasing = e.RightButton == MouseButtonState.Pressed;
			this.Draw(e);
		}

		private int last_modified_x = -1;
		private int last_modified_y = -1;

		private void Draw(MouseEventArgs e)
		{
			Point p = e.GetPosition(this.clicker_catcher);
			int x = (int)p.X;
			int y = (int)p.Y;
			int layer = Model.LayerCutoff;
			y -= this.RenderTop;
			x -= this.RenderMiddle;
			y += 8 * (layer + 1);
			int col = (y + x / 2) / 16;
			int row = (y - x / 2) / 16;
			this.LastX = col;
			this.LastY = row;

			if (this.isDrawing)
			{
				if (this.level.ModifyTile(col, row, layer, this.isErasing ? null : Model.ActiveTileSwatch))
				{
					this.level.IsDirty = true;
					this.Refresh();
				}
			}

			MainWindow.UpdateTitle();
		}

		void clicker_catcher_MouseMove(object sender, MouseEventArgs e)
		{
			this.Draw(e);
		}

		public int LastX { get; private set; }
		public int LastY { get; private set; }

		private int RenderTop { get { return 8 * 16 + 20; } }
		private int RenderMiddle { get { return this.level.Height * 16 + 20; } }

		public void Refresh()
		{
			this.tile_upper.Children.Clear();
			this.tile_lower.Children.Clear();
			int width = this.level.Width;
			int height = this.level.Height;
			// top center is 16 "layers"

			int top = this.RenderTop;
			int middle = this.RenderMiddle; ;
			int layerCutoff = Model.LayerCutoff;
			int x = 0;
			int y = 0;
			int pixelX, pixelY;
			for (int i = 0; i < width + height; ++i)
			{
				x = i;
				y = 0;
				pixelX = middle + i * 16;
				while (x >= 0)
				{
					pixelY = top + i * 8;
					if (x < width && y < height)
					{
						this.RenderTileStack(x, y, pixelX, pixelY, layerCutoff);
					}
					--x;
					++y;
					pixelX -= 32;
				}
			}
		}


		private enum RenderTarget
		{
			Lower,
			Upper,
			Cursor
		}

		public void RefreshHiddenOpacity()
		{
			this.tile_upper.Opacity = Model.IsHiddenLayersVisible ? .4 : 0;
		}

		private void Blit(ImageSource image, int pixelX, int pixelY, RenderTarget target)
		{
			Grid grid = this.tile_lower;
			if (target == RenderTarget.Cursor)
			{
				grid = this.tile_cursor;
			}
			else if (target == RenderTarget.Upper)
			{
				grid = this.tile_upper;
			}

			grid.Children.Add(
				new Image()
				{
					Source = image,
					Width = 32,
					Margin = new Thickness(pixelX, pixelY, 0, 0),
					HorizontalAlignment = System.Windows.HorizontalAlignment.Left,
					VerticalAlignment = System.Windows.VerticalAlignment.Top
				});
		}

		private void BlitTile(ImageSource image, int height, int pixelX, int pixelY, int cumulativeHeight, RenderTarget target)
		{
			this.Blit(image, pixelX - 16, pixelY - cumulativeHeight * 8 - height * 8, target);
		}

		private void RenderTileStack(int col, int row, int px, int py, int layerCutoff)
		{
			int cumulativeHeight = 0;
			List<Tile> tileStack = this.level.Grid[col + row * this.level.Width];
			bool inUpperLevel = false;

			BlitTile(this.foundationImage, 0, px, py + 1, cumulativeHeight, RenderTarget.Lower);

			foreach (Tile tile in tileStack)
			{
				int height = 1;
				if (tile != null)
				{
					BlitTile(tile.Image, tile.Height, px, py, cumulativeHeight, inUpperLevel ? RenderTarget.Upper : RenderTarget.Lower);
					height = tile.Height;
				}

				cumulativeHeight += height;
				if (cumulativeHeight > layerCutoff)
				{
					inUpperLevel = true;
				}
			}
		}
	}
}
