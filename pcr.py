import camp_incr as incr
import top_performers as perf
import percent_total as percent
import eaters as eat
import constants as const
import save_file as sf
    
camp_incr_dict = dict()
top_performer_dict = dict()
percent_total_dict = dict()
eaters_dict = dict()

if __name__ == "__main__":
    # global camp_incr_dict
    percent_total_dict = percent.summary_and_total_percent() 
    camp_incr_dict = incr.camp_incr_check()
    top_performer_dict = perf.top_performers()
    eaters_dict = eat.new_eaters_analysis()

    sf.write_excel(camp_incr_dict, percent_total_dict, eaters_dict, top_performer_dict)
    print("\nG-Sheet complete and Ready!")
    print("Preparing TLDR...")
    sf.write_doc(camp_incr_dict, percent_total_dict, eaters_dict, top_performer_dict)
    print("TLDR Complete!")

    

