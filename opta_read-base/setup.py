from opta_read.f27_function import F27


x=F27('C:/Users/Felix/Desktop/Máster  BD Deporte/Módulo 7 - Proveedores de Datos Deportivos/f27/pass_matrix_23_2019_g1074821_t957.xml')

pm=x.pass_matrix()
m_pos=x.mean_position_opta_f27()

x.plot_pass_meanpos(mean_position=m_pos,pass_matrix=pm, pass_color="green")
