import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Description
st.title("Data Product GUI with Robust Error Handling")
st.write("Upload a CSV file to explore, clean, and visualize your data.")

try:
    # Data Upload
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file
            st.subheader("Raw Data")
            data = pd.read_csv(uploaded_file)
            st.write(data)

            # Check if DataFrame is empty
            if data.empty:
                st.warning("The uploaded CSV is empty. Please provide a valid dataset.")
            else:
                # Data Exploration
                st.header("Data Exploration")

                # Display Summary Statistics
                st.subheader("Summary Statistics")
                try:
                    st.write(data.describe())
                except Exception as e:
                    st.error(f"Error calculating summary statistics: {e}")

                # Column Selection for Visualization
                st.subheader("Data Visualization")
                columns = data.columns.tolist()

                if len(columns) < 2:
                    st.warning("The CSV must have at least two columns for visualization.")
                else:
                    try:
                        x_axis = st.selectbox("Select X-axis", columns, key="x_axis")
                        y_axis = st.selectbox("Select Y-axis", columns, key="y_axis")

                        # Generate and Display Various Plots
                        if st.button("Generate Plots"):
                            try:
                                # Scatter Plot
                                fig, ax = plt.subplots()
                                ax.scatter(data[x_axis], data[y_axis], alpha=0.7)
                                ax.set_title(f"{y_axis} vs {x_axis} - Scatter Plot")
                                ax.set_xlabel(x_axis)
                                ax.set_ylabel(y_axis)
                                st.pyplot(fig)

                                # Line Plot
                                fig, ax = plt.subplots()
                                ax.plot(data[x_axis], data[y_axis], marker='o')
                                ax.set_title(f"{y_axis} vs {x_axis} - Line Plot")
                                ax.set_xlabel(x_axis)
                                ax.set_ylabel(y_axis)
                                st.pyplot(fig)

                                # Bar Plot
                                fig, ax = plt.subplots()
                                data.groupby(x_axis)[y_axis].mean().plot.bar(ax=ax)
                                ax.set_title(f"Average {y_axis} by {x_axis} - Bar Plot")
                                st.pyplot(fig)

                                # Histogram
                                fig, ax = plt.subplots()
                                data[y_axis].plot.hist(bins=20, alpha=0.7, ax=ax)
                                ax.set_title(f"Histogram of {y_axis}")
                                st.pyplot(fig)

                                # Box Plot
                                fig, ax = plt.subplots()
                                sns.boxplot(data=data, x=x_axis, y=y_axis, ax=ax)
                                ax.set_title(f"Box Plot of {y_axis} by {x_axis}")
                                st.pyplot(fig)

                                # Violin Plot
                                fig, ax = plt.subplots()
                                sns.violinplot(data=data, x=x_axis, y=y_axis, ax=ax)
                                ax.set_title(f"Violin Plot of {y_axis} by {x_axis}")
                                st.pyplot(fig)

                                # Heatmap (Correlation Matrix)
                                fig, ax = plt.subplots()
                                corr = data.corr()
                                sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                                ax.set_title("Correlation Heatmap")
                                st.pyplot(fig)

                                # Pairplot (Scatterplot Matrix)
                                try:
                                    st.write("Scatterplot Matrix")
                                    sns.pairplot(data, diag_kind='kde')
                                    st.pyplot()
                                except Exception as e:
                                    st.error(f"Error generating scatterplot matrix: {e}")

                                # Pie Chart (for categorical data)
                                if len(data[x_axis].unique()) <= 10:  # Limit to 10 categories for pie chart
                                    fig, ax = plt.subplots()
                                    data[x_axis].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                                    ax.set_ylabel("")
                                    ax.set_title(f"Distribution of {x_axis}")
                                    st.pyplot(fig)

                                # KDE Plot
                                fig, ax = plt.subplots()
                                sns.kdeplot(data[y_axis], ax=ax)
                                ax.set_title(f"KDE Plot of {y_axis}")
                                st.pyplot(fig)

                            except KeyError as ke:
                                st.error(f"Invalid key selection for plotting: {ke}")
                            except Exception as e:
                                st.error(f"An error occurred while generating the plots: {e}")
                    except Exception as e:
                        st.error(f"Error in selecting columns for visualization: {e}")

                # Data Cleaning and Preprocessing
                st.header("Data Cleaning")

                # Handle Missing Values
                st.subheader("Handle Missing Values")
                try:
                    missing_option = st.radio(
                        "Choose how to handle missing values:",
                        ["Do Nothing", "Drop Rows with Missing Values", "Fill with Zero"]
                    )

                    if missing_option == "Drop Rows with Missing Values":
                        data = data.dropna()
                        st.write("Rows with missing values have been removed.")
                        st.write(data)
                    elif missing_option == "Fill with Zero":
                        data = data.fillna(0)
                        st.write("Missing values have been filled with zeros.")
                        st.write(data)
                except Exception as e:
                    st.error(f"An error occurred while handling missing values: {e}")

                # Remove Duplicates
                st.subheader("Remove Duplicates")
                if st.button("Remove Duplicates"):
                    try:
                        data = data.drop_duplicates()
                        st.write("Duplicate rows have been removed.")
                        st.write(data)
                    except Exception as e:
                        st.error(f"An error occurred while removing duplicates: {e}")

                # Export Cleaned Data
                st.subheader("Export Cleaned Data")
                try:
                    if st.button("Download CSV"):
                        # Create CSV in memory
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label="Download Cleaned Data as CSV",
                            data=csv,
                            file_name="cleaned_data.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"An error occurred while preparing the CSV for download: {e}")

        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file appears to be empty. Please upload a valid CSV file.")
        except pd.errors.ParserError:
            st.error("There was an error parsing the CSV file. Please ensure the file is properly formatted.")
        except Exception as e:
            st.error(f"An unexpected error occurred while loading the CSV file: {e}")

    else:
        st.write("Please upload a CSV file to proceed.")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
