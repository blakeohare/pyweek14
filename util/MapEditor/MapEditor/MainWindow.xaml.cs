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
			this.InitializeLayerPicker(0);
			this.tile_category_picker.SelectedIndex = 0;
			this.KeyDown += new KeyEventHandler(MainWindow_KeyDown);
			this.layer_picker.SelectionChanged += new SelectionChangedEventHandler(layer_picker_SelectionChanged);
			this.AddMenuHandlers();
		}

		private LevelRenderer ActiveLevelRenderer
		{
			get { return this.render_host.Children[0] as LevelRenderer; }
		}

		void layer_picker_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			int foo = this.ActiveLayer;
			if (Model.ActiveLevel != null)
			{
				this.ActiveLevelRenderer.Refresh();
			}
		}

		private void AddMenuHandlers()
		{
			this.menu_file_exit.Click += new RoutedEventHandler(menu_file_exit_Click);
			this.menu_file_new.Click += new RoutedEventHandler(menu_file_new_Click);
			this.menu_file_save.Click += new RoutedEventHandler(menu_file_save_Click);
			this.menu_file_open.Click += new RoutedEventHandler(menu_file_open_Click);
			this.menu_file_revert.Click += new RoutedEventHandler(menu_file_revert_Click);
			this.menu_stuff_down.Click += new RoutedEventHandler(menu_stuff_down_Click);
			this.menu_stuff_up.Click += new RoutedEventHandler(menu_stuff_up_Click);
			this.menu_stuff_duke.Click += new RoutedEventHandler(menu_stuff_duke_Click);
		}

		void menu_stuff_duke_Click(object sender, RoutedEventArgs e)
		{
			Model.IsHiddenLayersVisible = !Model.IsHiddenLayersVisible;
			this.ActiveLevelRenderer.RefreshHiddenOpacity();
		}

		private void AdjustPickedLayer(int amount)
		{
			int index = this.layer_picker.SelectedIndex + amount;
			int max = this.layer_picker.Items.Count;
			index = index < 0 ? 0 : index;
			index = index >= max ? max - 1 : index;
			this.InitializeLayerPicker(index);
			//this.layer_picker.SelectedIndex = index;
			//this.layer_picker.SelectedItem = this.layer_picker.Items[index];
			//this.layer_picker.SelectedValue = "Layer " + index;
			//this.layer_picker_SelectionChanged(null, null);
		}

		

		private int ActiveLayer
		{
			get
			{
				string value = (this.layer_picker.SelectedValue ?? "Layer 0").ToString();
				return int.Parse(value.Split(' ')[1]);
			}
		}

		public static int LayerCutoff
		{
			get { return instance.ActiveLayer; }
		}

		void menu_stuff_up_Click(object sender, RoutedEventArgs e)
		{
			this.AdjustPickedLayer(1);
		}

		void menu_stuff_down_Click(object sender, RoutedEventArgs e)
		{
			this.AdjustPickedLayer(-1);
		}

		void menu_file_revert_Click(object sender, RoutedEventArgs e)
		{
			if (Model.ActiveLevel != null)
			{
				Level level = new Level(Model.ActiveLevel.Name, false);
				this.MakeThisLevelActive(level);
			}
		}

		private void InitializeLayerPicker(int selectedIndex)
		{
			this.layer_picker.Items.Clear();
			for (int i = 0; i <= 30; ++i) {
				this.layer_picker.Items.Add("Layer " + i.ToString());
			}
			this.layer_picker.SelectedItem = this.layer_picker.Items[selectedIndex];
			//this.layer_picker.SelectedIndex = selectedIndex;
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
			else if (e.Key == Key.D && ctrl)
			{
				this.menu_stuff_duke_Click(null, null);
			}
			else if (e.Key == Key.F5)
			{
				this.menu_file_revert_Click(null, null);
			}
			else if (e.Key == Key.OemPlus || e.Key == Key.Add)
			{
				this.AdjustPickedLayer(1);
			}
			else if (e.Key == Key.OemMinus || e.Key == Key.Subtract)
			{
				this.AdjustPickedLayer(-1);
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
