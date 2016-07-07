import psycopg2
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np
from decimal import *

class ReadAllRecords:

    @staticmethod
    def cc(arg):
        return colorConverter.to_rgba(arg, alpha=0.6)

    def demo(self):

        conn = psycopg2.connect(database="related", user="amishra", password="", host="127.0.0.1", port="5432")
        print "Opened database successfully"

        cur = conn.cursor()

        query = """ select  de_country  , de_dc_company_name, month ,  sum(counter) from industry_wise
        where industry = 'MEDICAL'
        group by de_country ,de_dc_company_name , month
        order by de_country  ,de_dc_company_name, month  """

        cur.execute(query)
        rows = cur.fetchall()
        prev_country = ""
        country = ""
        country_num = 1
        cmp_name = ""
        prev_cmp_name = ""
        company_num = 1

        # company = []
        month = np.arange(0, 18, 1)
        search_count = [0] * 18
        company_stats = {}

        for row in rows:
            country = row[0]

            if prev_country == "":
                prev_country = country

            if country == prev_country:
                # we are in the same country
                cmp_name = row[1]

                if prev_cmp_name == "":
                    prev_cmp_name = cmp_name

                if cmp_name == prev_cmp_name:
                    # we are in the same company, fetch the count and set it for the month
                    temp = row[2]
                    if temp > 201600:
                        temp = temp - 201601 + 12
                    else:
                        temp = temp - 201501
                    final_val = int((row[3]).to_integral_value())
                    search_count[temp] = final_val

                else:
                    # we have found a new company
                    print prev_cmp_name, search_count
                    # store the search count for the given company
                    company_stats[company_num] = search_count
                    #clean the searh_count for the new incoming company
                    search_count = [0] * 18
                    # increment the company_count and update the prev_cmp_name
                    company_num += 1
                    prev_cmp_name = cmp_name
                    # store the incoming count value
                    temp = row[2]
                    if temp > 201600:
                        temp = temp - 201601 + 12
                    else:
                        temp = temp - 201501
                    final_val = int((row[3]).to_integral_value())
                    search_count[temp] = final_val

            else:
                # the country was changed. So the company has changes inherently
                print prev_cmp_name, search_count
                company_stats[company_num] = search_count
                print company_stats.keys()
                print "THE LAST COUNTRY WAS:" + prev_country.upper()
                # Plot the figure for the given country
                fig = plt.figure(country_num)
                fig.suptitle(prev_country.upper(), fontsize=20)
                country_num += 1
                ax = fig.gca(projection='3d')
                global_max = 0
                xs = month
                verts = []
                zs = company_stats.keys()
                for z in company_stats.keys():
                    ys = company_stats[z]
                    ys = [0, 0] + ys + [0, 0]
                    local_max = max(ys)
                    if local_max > global_max:
                        global_max = local_max
                    verts.append(list(zip(xs, ys)))
                poly = PolyCollection(verts, closed=False)
                poly.set_alpha(0.6)
                ax.add_collection3d(poly, zs=zs, zdir='y')
                ax.set_xlim3d(0-2, 18+2)
                ax.set_ylim3d(-1, company_num + 1)
                ax.set_zlim3d(0 , global_max + int ((global_max + 1 - 0) * 0.1))
                # Plotting code ends
                print "&&&&&&&&&&&&&&&&&& THE COUNTRY HAS CHANGED &&&&&&&&&&&&&&&&"



                # Clean up
                company_stats = {}
                search_count = [0] * 18
                cmp_name = row[1]
                prev_cmp_name = row[1]
                company_num = 1
                prev_country = country

                # store the incoming count value
                temp = row[2]
                if temp > 201600:
                    temp = temp - 201601 + 12
                else:
                    temp = temp - 201501
                final_val = int((row[3]).to_integral_value())
                search_count[temp] = final_val

        # Some records will still be present from the last comany read which did not change but the cursor was done
        print cmp_name, search_count
        company_stats[company_num] = search_count
        print company_stats.keys()
        print "THE LAST COUNTRY WAS:" + prev_country.upper()
        print "Operation done successfully"

        # Plotting code start
        # Plotting code ends


        conn.close()
        plt.show()

        # fig = plt.figure()
        # ax = fig.gca(projection='3d')
        #
        #
        # xs = np.arange(0, 10, 0.4)
        # verts = []
        # zs = [0.0, 1.0, 2.0, 3.0]
        # for z in zs:
        #     ys = np.random.rand(len(xs))
        #     ys[0], ys[-1] = 0, 0
        #     verts.append(list(zip(xs, ys)))
        #
        # poly = PolyCollection(verts, facecolors=[ReadAllRecords.cc('r'), ReadAllRecords.cc('g'), ReadAllRecords.cc('b'),
        #                                          ReadAllRecords.cc('y')])
        # # poly = PolyCollection(verts)
        # poly.set_alpha(0.6)
        # ax.add_collection3d(poly, zs=zs, zdir='y')
        #
        # ax.set_xlabel('X')
        # ax.set_xlim3d(0, 10)
        # ax.set_ylabel('Y')
        # ax.set_ylim3d(-1, 4)
        # ax.set_zlabel('Z')
        # ax.set_zlim3d(0, 1)
        #
        # plt.show()


        # t = np.arange(0.0, 2.0, 0.01)
        # s1 = np.sin(2 * np.pi * t)
        # s2 = np.sin(4 * np.pi * t)
        #
        # plt.figure(1)
        # plt.subplot(211)
        # plt.plot(t, s1)
        # plt.subplot(212)
        # plt.plot(t, 2 * s1)
        #
        # plt.figure(2)
        # plt.plot(t, s2)
        #
        # # now switch back to figure 1 and make some changes
        # plt.figure(1)
        # plt.subplot(211)
        # plt.plot(t, s2, 'gs')
        # ax = plt.gca()
        # ax.set_xticklabels([])
        #
        # plt.show()




ReadAllRecords().demo()
