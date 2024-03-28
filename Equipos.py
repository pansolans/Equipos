import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from soccerplots.radar_chart import Radar


def load_data():
    path = 'b Nacional.xlsx'  # Asegúrate de ajustar la ruta según sea necesario
    return pd.read_excel(path)

df = load_data()

# Configurar el estilo de Matplotlib para el gráfico de dispersión
plt.style.use('dark_background')

# Inicializar las pestañas
tab1, tab2 = st.tabs(["Gráfico de Dispersión", "Gráfico Radar"])

# Pestaña para el gráfico de dispersión
with tab1:
    st.title('Comparación de Equipos - Gráfico de Dispersión')

    # Seleccionar variables para los ejes X e Y
    x_axis = st.selectbox('Selecciona la variable para el eje X:', df.columns, index=df.columns.get_loc('possessionPercent'))
    y_axis = st.selectbox('Selecciona la variable para el eje Y:', df.columns, index=df.columns.get_loc('goals'))

    # Selector para excluir etiquetas de nombres de equipos del gráfico
    excluded_teams_for_labels = st.multiselect('Selecciona los equipos cuyos nombres quieres excluir del gráfico:', df['name'].unique())

    # Crear el gráfico de dispersión
    fig, ax = plt.subplots(figsize=(10, 6))
    plot = sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax, s=50, color='cyan', edgecolor='none')

    # Ajustes adicionales del gráfico
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.tick_params(colors='white', which='both')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')

    # Calcular y dibujar líneas de promedio
    x_mean = df[x_axis].mean()
    y_mean = df[y_axis].mean()
    ax.axhline(y=y_mean, color='#b6ccd8', linestyle='--', label=f'Promedio {y_axis}: {y_mean:.2f}')
    ax.axvline(x=x_mean, color='#d4eaf7', linestyle='--', label=f'Promedio {x_axis}: {x_mean:.2f}')

    # Agregar etiquetas solo para equipos no excluidos
    for i in range(df.shape[0]):
        if df['name'].iloc[i] not in excluded_teams_for_labels:
            ax.text(df[x_axis].iloc[i], df[y_axis].iloc[i], df['name'].iloc[i], fontsize=8, ha='right', va='bottom', color='white')

    # Configuración para colocar la leyenda debajo del gráfico
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False, fontsize='small')

    st.pyplot(fig)



# Pestaña para el gráfico radar
with tab2:
    plt.style.use('default')
    st.title('Comparación de Equipos de Fútbol - Gráfico Radar')

    # Selección de equipos y estadísticas para comparar
    selected_teams = st.multiselect('Selecciona dos equipos para comparar:', df['name'].unique(), default=df['name'].unique()[:2])
    selected_stats = st.multiselect('Selecciona las estadísticas para comparar:', df.columns.tolist(), default=df.columns.tolist()[1:6])

    if len(selected_teams) == 2 and len(selected_stats) > 0:
        df_filtered = df[df['name'].isin(selected_teams)][['name'] + selected_stats]
        params = selected_stats
        values = []
        ranges = [(df_filtered[stat].min() - (df_filtered[stat].min() * 0.1), df_filtered[stat].max() + (df_filtered[stat].max() * 0.1)) for stat in selected_stats]

        for team in selected_teams:
            values.append(df_filtered[df_filtered['name'] == team].iloc[0, 1:].values.tolist())

        # Configuración de título para el gráfico radar
        title = {
            'title_name': selected_teams[0],
            'title_color': '#1d2e3d',
            'subtitle_color': 'red',
            'title_name_2': selected_teams[1],
            'title_color_2': '#0D6E6E',
            'subtitle_color_2': 'blue',
            'title_fontsize': 18,
            'subtitle_fontsize': 15,
        }

        radar = Radar()
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values,
                                   radar_color=['#1d2e3d', '#0D6E6E'],
                                   alphas=[.75, .6], title=title,
                                   endnote='Secretaría Técnica de Quilmes',
                                   compare=True)
        st.pyplot(fig)
    else:
        st.error('Por favor, selecciona exactamente dos equipos y al menos una estadística para la comparación.')
