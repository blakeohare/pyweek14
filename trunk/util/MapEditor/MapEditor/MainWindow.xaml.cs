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
			this.tile_category_picker.SelectedIndex = 0;
			this.menu_file_exit.Click += new RoutedEventHandler(menu_file_exit_Click);
			this.menu_file_new.Click += new RoutedEventHandler(menu_file_new_Click);
			this.menu_file_save.Click += new RoutedEventHandler(menu_file_save_Click);
			this.menu_file_open.Click += new RoutedEventHandler(menu_file_open_Click);
			this.KeyDown += new KeyEventHandler(MainWindow_KeyDown);
		}

		private void menu_file_open_Click(object sender, RoutedEventArgs e)
		{
			OpenLevelDialog old = new OpenLevelDialog();
			old.ShowDialog();
			if (old.Status)
			{
				Level level = new Level(old.Level, false);
				this.MakeThisLevelActive(level);
			}
		}

		void MainWindow_KeyDown(object sender, KeyEventArgs e)
		{
			bool alt = (System.Windows.Input.Keyboard.Modifiers & ModifierKeys.Alt) != 0;
			bool ctrl = (System.Windows.Input.Keyboard.Modifiers & ModifierKeys.Control) != 0;
			bool shift = (System.Windows.Input.Keyboard.Modifiers & ModifierKeys.Shift) != 0;

			if (e.Key == Key.N && ctrl)
			{
				this.menu_file_new_Click(null, null);
			}
			else if (e.Key == Key.O && ctrl)
			{
				this.menu_file_open_Click(null, null);
			}
			else if (e.Key == Key.S && ctrl)
			{
				this.menu_file_save_Click(null, null);
			}
		}

		void menu_file_save_Click(object sender, RoutedEventArgs e)
		{
			Level activeLevel = Model.ActiveLevel;
			if (activeLevel != null)
			{
				activeLevel.Save();
			}
		}

		void menu_file_new_Click(object sender, RoutedEventArgs e)
		{
			NewLevelDialog nld = new NewLevelDialog();
			nld.ShowDialog();
			if (nld.Status)
			{
				string name = nld.LevelName;
				if (name.Length == 0)
				{
					MessageBox.Show("Cannot have a blank name");
				}
				else
				{
					Level level = new Level(name, true);
					this.MakeThisLevelActive(level);
				}
			}
			
		}

		private void MakeThisLevelActive(Level level)
		{
			Model.ActiveLevel = level;
			LevelRenderer renderer = new LevelRenderer(level);
			renderer.Refresh();
			this.render_host.Children.Clear();
			this.render_host.Children.Add(renderer);
		}

		void menu_file_exit_Click(object sender, RoutedEventArgs e)
		{
			// TODO: prompt for save
			this.Close();
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
