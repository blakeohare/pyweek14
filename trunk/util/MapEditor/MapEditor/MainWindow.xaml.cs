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
	/// Interaction logic for MainWindow.xaml
	/// </summary>
	public partial class MainWindow : Window
	{
		private static MainWindow instance;
		public MainWindow()
		{
			instance = this;
			InitializeComponent();
			TileStore.Initialize();
			this.InitializeTileCategoryPickerChoices();
		}

		private void InitializeTileCategoryPickerChoices()
		{
			foreach (string category in TileStore.GetSortedCategories())
			{
				this.tile_category_picker.Items.Add(category);
			}
			this.tile_category_picker.SelectionChanged += new SelectionChangedEventHandler(tile_category_picker_SelectionChanged);
		}

		private void tile_category_picker_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			this.RefreshTileSwatches();
		}

		private void RefreshTileSwatches()
		{
			this.tile_swatches.Children.Clear();
			string category = (this.tile_category_picker.SelectedValue ?? "").ToString();
			if (category.Length > 0)
			{
				foreach (Tile t in TileStore.GetSortedTilesForCategory(category))
				{
					TileSwatch ts = new TileSwatch(t);
					ts.UpdateSelectionVisual();
					this.tile_swatches.Children.Add(ts);
				}
			}
		}

		public static void UpdateSwatchSelection()
		{
			foreach (TileSwatch swatches in instance.tile_swatches.Children.OfType<TileSwatch>())
			{
				swatches.UpdateSelectionVisual();
			}
		}
	}
}
