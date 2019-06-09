from database import execute_query
from models import Country, City, Rank, NationalRank, Player, Tournament, Participant, Pairing


def select_pairing_query(tournament_id, player_id=None):
    query = f"""
SELECT
    tp.id, tp.place, tp.rating_start, tp.rating_end, 

    t.id, t.name, t.PIN, t.date_start, t.date_end, t.is_ranked,
    tc.id, tc.name,
    tc2.id, tc2.name, tc2.code,

    p.id, p.last_name, p.first_name, p.PIN, p.rating, p.is_active, 
    c.id, c.name, 
    c2.id, c2.name, c2.code,
    r.id, r.name, r.abbreviate, 
    nr.id, nr.name, nr.abbreviate,

    r2.id, r2.name, r2.abbreviate, 

    tg.id, tg.round, tg.color, tg.handicap, tg.result, tg.round_skip, tg.is_technical,

    tp2.id, tp2.place, tp2.rating_start, tp2.rating_end, 

    p2.id, p2.last_name, p2.first_name, p2.PIN, p2.rating, p2.is_active, 
    c3.id, c3.name, 
    c4.id, c4.name, c4.code,
    r3.id, r3.name, r3.abbreviate, 
    nr2.id, nr2.name, nr2.abbreviate,

    r4.id, r4.name, r4.abbreviate

FROM participant tp

INNER JOIN tournament t ON tp.tournament_id=t.id
LEFT JOIN city tc ON t.city_id=tc.id
LEFT JOIN country tc2 ON tc.country_id=tc2.id

INNER JOIN player p ON tp.player_id=p.id
LEFT JOIN city c ON p.city_id=c.id
LEFT JOIN country c2 ON c.country_id=c2.id 
LEFT JOIN rank r ON p.rank_id=r.id
LEFT JOIN national_rank nr ON p.national_rank_id=nr.id

LEFT JOIN rank r2 ON tp.rank_id=r2.id

INNER JOIN pairing tg ON tg.player_id=tp.id

LEFT JOIN participant tp2 ON tg.opponent_id=tp2.id

LEFT JOIN player p2 ON tp2.player_id=p2.id
LEFT JOIN city c3 ON p2.city_id=c3.id
LEFT JOIN country c4 ON c3.country_id=c4.id 
LEFT JOIN rank r3 ON p2.rank_id=r3.id
LEFT JOIN national_rank nr2 ON p2.national_rank_id=nr2.id

LEFT JOIN rank r4 ON tp2.rank_id=r4.id

WHERE tp.tournament_id = {tournament_id}
"""
    if player_id:
        query += f"AND p1.id = {player_id}\n"

    query += 'ORDER BY tp.place ASC, tg.round ASC'
    result = execute_query(query)

    pairings = []
    for (
            tp1_id, tp_place, tp1_rating_start, tp1_rating_end,

            t_id, t_name, t_PIN, t_date_start, t_date_end, t_is_ranked,
            tc_id, tc_name,
            tc2_id, tc2_name, tc2_code,

            p1_id, p1_last_name, p1_first_name, p1_PIN, p1_rating, p1_is_active,
            c1_id, c1_name,
            c2_id, c2_name, c2_code,
            r1_id, r1_name, r1_abbreviate,
            nr1_id, nr1_name, nr1_abbreviate,

            r2_id, r2_name, r2_abbreviate,

            tg_id, tg_round, tg_color, tg_handicap, tg_result, tg_round_skip, tg_is_technical,

            tp2_id, tp2_place, tp2_rating_start, tp2_rating_end,

            p2_id, p2_last_name, p2_first_name, p2_PIN, p2_rating, p2_is_active,
            c3_id, c3_name,
            c4_id, c4_name, c4_code,
            r3_id, r3_name, r3_abbreviate,
            nr2_id, nr2_name, nr2_abbreviate,

            r4_id, r4_name, r4_abbreviate
    ) in result:
        tournament_country = Country(tc2_id, tc2_name, tc2_code)
        tournament_city = City(tc_id, tc_name, tournament_country)

        tournament = Tournament(t_id, t_name, t_PIN, t_date_start, t_date_end, t_is_ranked, tournament_city)

        country1 = Country(c2_id, c2_name, c2_code)
        city1 = City(c1_id, c1_name, country1)
        rank1 = Rank(r1_id, r1_name, r1_abbreviate)
        national_rank1 = NationalRank(nr1_id, nr1_name, nr1_abbreviate)
        player1 = Player(p1_id, p1_last_name, p1_first_name, p1_PIN, p1_rating, p1_is_active, city1, rank1,
                         national_rank1)

        participant_rank = Rank(r2_id, r2_name, r2_abbreviate)
        participant = Participant(tp1_id, player1, tournament, tp_place, participant_rank, tp1_rating_start,
                                  tp1_rating_end)

        country2 = Country(c4_id, c4_name, c4_code)
        city2 = City(c3_id, c3_name, country2)
        rank2 = Rank(r3_id, r3_name, r3_abbreviate)
        national_rank2 = NationalRank(nr2_id, nr2_name, nr2_abbreviate)
        player2 = Player(p2_id, p2_last_name, p2_first_name, p2_PIN, p2_rating, p2_is_active, city2, rank2,
                         national_rank2)

        opponent_rank = Rank(r4_id, r4_name, r4_abbreviate)
        opponent = Participant(tp2_id, player2, tournament, tp2_place, opponent_rank, tp2_rating_start, tp2_rating_end)

        pairing = Pairing(tg_id, participant, tg_round, opponent, tg_color, tg_handicap, tg_result, tg_round_skip,
                          tg_is_technical)
        pairings.append(pairing)

    return pairings