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
using System.Windows.Shapes;

namespace MapEditor
{
	/// <summary>
	/// Interaction logic for ResizeDialog.xaml
	/// </summary>
	public partial class ResizeDialog : Window
	{
		public bool Status { get; private set; }
		public ResizeDialog(Level level)
		{
			InitializeComponent();
			this.current_dimensions.Text = "Current dimensions: " + level.Width.ToString() + " by " + level.Height.ToString();
			this.new_width.Text = level.Width.ToString();
			this.new_height.Text = level.Height.ToString();
			this.ok_button.Click += new RoutedEventHandler(ok_button_Click);
			this.cancel_button.Click += new RoutedEventHandler(cancel_button_Click);
			this.anchor_to.SelectedIndex = 1;
		}

		void cancel_button_Click(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

		public string Anchor { get; private set; }
		public int NewWidth { get; private set; }
		public int NewHeight { get; private set; }
		void ok_button_Click(object sender, RoutedEventArgs e)
		{
			int width = -1;
			int height = -1;

			if (!int.TryParse(this.new_width.Text, out width))
			{
				MessageBox.Show("Invalid width");
			}
			else if (!int.TryParse(this.new_height.Text, out height))
			{
				MessageBox.Show("Invalid height");
			}
			else
			{
				string anchor = (((ComboBoxItem)this.anchor_to.SelectedValue).Content ?? "").ToString().ToLower();
				if (anchor != "bottom" && anchor != "top" && anchor != "left" && anchor != "right")
				{
					MessageBox.Show("Invalid anchor");
				}
				else
				{
					this.Anchor = anchor;
					this.Status = true;
					this.NewWidth = width;
					this.NewHeight = height;
					this.Close();
				}
			}
		}
	}
}
