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
	/// Interaction logic for TileSwatch.xaml
	/// </summary>
	public partial class TileSwatch : UserControl
	{
		public Tile Tile { get; private set; }
		public TileSwatch(Tile tile)
		{
			this.Tile = tile;
			InitializeComponent();
			this.image_swatch.Source = tile.Image;
			string label = tile.ImageFiles[0];
			this.text_label.Text = label.Substring("images/tiles/".Length);
			this.MouseLeftButtonDown += new MouseButtonEventHandler(TileSwatch_MouseLeftButtonDown);
		}

		void TileSwatch_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			Model.ActiveTileSwatch = this.Tile;
			MainWindow.UpdateSwatchSelection();
		}

		public void UpdateSelectionVisual()
		{
			bool selected = Model.ActiveTileSwatch == this.Tile;
			Brush background = selected ? Brushes.Navy : Brushes.White;
			Brush foreground = selected ? Brushes.White : Brushes.Black;

			this.layoutroot.Background = background;
			this.text_label.Foreground = foreground;
		}
	}
}
