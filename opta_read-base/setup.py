from opta_read.f27_function import F27
from opta_read.f30_function import F30
from opta_read.f28_function import F28
from opta_read.f71_function import F71


# x=F27('C:/Users/Felix/Desktop/Máster  BD Deporte/Módulo 7 - Proveedores de Datos Deportivos/f27/pass_matrix_23_2019_g1074821_t957.xml')

# pm=x.pass_matrix()
# m_pos=x.mean_position_opta_f27()

# x.plot_pass_meanpos(mean_position=m_pos,pass_matrix=pm, pass_color="green")


# x=F30('C:/Users/Felix/Desktop/Máster  BD Deporte/Módulo 7 - Proveedores de Datos Deportivos/f30/seasonstats-23-2019-174.xml')
# team=x.team_stats()
# # print(team)

# players=x.players_stats()
# # print(players)

# ## Following function only works properly in jupyter
# x.compare_players(players,["Yuri Berchiche Izeta","Ander Capa"] ,["Goals", 'Total Passes', 'Successful Dribbles', 'Total Shots'],"red","green")

# x=F28('C:/Users/Felix/Desktop/Máster  BD Deporte/Módulo 7 - Proveedores de Datos Deportivos/f28/f28-23-2019-1074825-eventdetails.xml')

# poss=x.possesion(possesion_type="BallPossession",interval_length=5)

# x.pitch_possesion_evolution(poss, animated=False)

# x.line_possesion_evolution(poss)
x=F71('C:/Users/Felix/Desktop/Máster  BD Deporte/Módulo 7 - Proveedores de Datos Deportivos/Liga Primera 23/f71/f71-23-2022-2301587-defcoverage.xml')
stat=x.defensive_stats()
x.plot_defensive_coverages(stat,team="Mallorca")
