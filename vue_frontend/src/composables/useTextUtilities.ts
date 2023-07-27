// import { CertifiedStatus, CommunicationMethod, LegalStatus, LocationType } from "@/types/Operation";
// import { Scope } from "@/types/Commodity";
// import { InquiryType, ResponseType } from "@/types/Inquiry";
// import { USState, Country } from "@/types/Geography";


export default function useTextUtilities() {
    // function enumVerbose(text: string) {
    //     return (text in enumDict) ? enumDict[text] : "-";
    // }

    // function enumAsObject<T>(someEnum: T) {
    //     const dict = {} as Record<string, string>;
    //     for (const key of Object.values(someEnum)) {
    //         if (key in enumDict) dict[key] = enumDict[key];
    //     }
    //     return dict;
    // }

    // function parseDate(text: string) {
    //     const elapsed = Date.parse(text);
    //     return elapsed ? new Date(elapsed) : undefined;
    // }

    // function formatDate(date: Date) {
    //     if (!date) return "-";
    //     const yyyy = date.getFullYear();
    //     const mm = date.getMonth() + 1; //0 based
    //     const dd = date.getDate();
    //     return `${yyyy}-${mm}-${dd}`;
    // }

    // function formatCurrency(dollars: number) { //, currency="USD") {
    //     return "$" + dollars.toLocaleString("en-US").replace(/\.00$/, "");
    // }
    
    // const enumDict = {
    //     [CertifiedStatus.PROSPECT]: "Prospect",
    //     [CertifiedStatus.IN_PROCESS]: "In Process",
    //     [CertifiedStatus.CERTIFIED]: "Certified",
    //     [CertifiedStatus.FORMER]: "Former",
    //     [CertifiedStatus.SURRENDERED]: "Surrendered",
    //     [CertifiedStatus.SUSPENDED]: "Suspended",
    //     [CertifiedStatus.REINSTATING]: "Reinstating",
    //     [CertifiedStatus.REVOKED]: "Revoked",
    //     [CertifiedStatus.DENIED]: "Denied",
    //     [CertifiedStatus.WITHDRAWN]: "Withdrawal",

    //     [CommunicationMethod.EMAIL]: "Email",
    //     [CommunicationMethod.PAPER]: "Paper",

    //     [LegalStatus.INDIVIDUAL]: "Individual",
    //     [LegalStatus.COOPERATIVE]: "Cooperative",
    //     [LegalStatus.PARTNERSHIP]: "Partnership",
    //     [LegalStatus.CORPORATION]: "Corporation",
    //     [LegalStatus.ASSOCIATION]: "Association",
    //     [LegalStatus.LLC]: "LLC",
    //     [LegalStatus.OTHER]: "Other",

    //     [LocationType.PRIMARY]: "Primary",
    //     [LocationType.ADDITIONAL]: "Additional",
    //     [LocationType.MAILING]: "Mailing",
    //     [LocationType.OTHER]: "Other",
    //     [LocationType.LAND]: "Land",

    //     [Scope.CROP]: "Crop",
    //     [Scope.WILD_CROP]: "Wild Crop",
    //     [Scope.LIVESTOCK]: "Livestock",
    //     [Scope.HANDLER]: "Handling",

    //     [InquiryType.OSP]: "OSP",
    //     [InquiryType.REVIEW]: "Certification Review",
    //     [InquiryType.ADMIN]: "Client Admin",

    //     [ResponseType.SMALL_TEXT]: "Text",
    //     [ResponseType.BIG_TEXT]: "Big Text",
    //     [ResponseType.DATE]: "Date",
    //     [ResponseType.TIME]: "Time",
    //     [ResponseType.DATE_TIME]: "Date and Time",
    //     [ResponseType.NUMBER]: "Number",
    //     [ResponseType.YES_NO]: "Yes/No",
    //     [ResponseType.YES_NO_NA]: "Yes/No/NA",
    //     // [ResponseType.FILE]: "File",
    //     [ResponseType.CHECKBOX]: "Multi Select",
    //     [ResponseType.RADIO]: "Single Select",
    //     [ResponseType.DROPDOWN]: "Dropdown",
    //     [ResponseType.TABLE]: "Table",
    //     [ResponseType.NONE]: "None",




    //     [USState.ALASKA]: "Alaska",
    //     [USState.ALABAMA]: "Alabama",
    //     [USState.ARKANSAS]: "Arkansas",
    //     [USState.ARIZONA]: "Arizona",
    //     [USState.CALIFORNIA]: "California",
    //     [USState.COLORADO]: "Colorado",
    //     [USState.CONNECTICUT]: "Connecticut",
    //     [USState.DC]: "District Of Columbia",
    //     [USState.DELAWARE]: "Delaware",
    //     [USState.FLORIDA]: "Florida",
    //     [USState.GEORGIA]: "Georgia",
    //     [USState.HAWAII]: "Hawaii",
    //     [USState.IOWA]: "Iowa",
    //     [USState.IDAHO]: "Idaho",
    //     [USState.ILLINOIS]: "Illinois",
    //     [USState.INDIANA]: "Indiana",
    //     [USState.KANSAS]: "Kansas",
    //     [USState.KENTUCKY]: "Kentucky",
    //     [USState.LOUISIANA]: "Louisiana",
    //     [USState.MASSACHUSETTS]: "Massachusetts",
    //     [USState.MARYLAND]: "Maryland",
    //     [USState.MAINE]: "Maine",
    //     [USState.MICHIGAN]: "Michigan",
    //     [USState.MINNESOTA]: "Minnesota",
    //     [USState.MISSOURI]: "Missouri",
    //     [USState.MISSISSIPPI]: "Mississippi",
    //     [USState.MONTANA]: "Montana",
    //     [USState.NORTH_CAROLINA]: "North Carolina",
    //     [USState.NORTH_DAKOTA]: "North Dakota",
    //     [USState.NEBRASKA]: "Nebraska",
    //     [USState.NEW_HAMPSHIRE]: "New Hampshire",
    //     [USState.NEW_JERSEY]: "New Jersey",
    //     [USState.NEW_MEXICO]: "New Mexico",
    //     [USState.NEVADA]: "Nevada",
    //     [USState.NEW_YORK]: "New York",
    //     [USState.OHIO]: "Ohio",
    //     [USState.OKLAHOMA]: "Oklahoma",
    //     [USState.OREGON]: "Oregon",
    //     [USState.PENNSYLVANIA]: "Pennsylvania",
    //     [USState.RHODE_ISLAND]: "Rhode Island",
    //     [USState.SOUTH_CAROLINA]: "South Carolina",
    //     [USState.SOUTH_DAKOTA]: "South Dakota",
    //     [USState.TENNESSEE]: "Tennessee",
    //     [USState.TEXAS]: "Texas",
    //     [USState.UTAH]: "Utah",
    //     [USState.VIRGINIA]: "Virginia",
    //     [USState.VERMONT]: "Vermont",
    //     [USState.WASHINGTON]: "Washington",
    //     [USState.WISCONSIN]: "Wisconsin",
    //     [USState.WEST_VIRGINIA]: "West Virginia",
    //     [USState.WYOMING]: "Wyoming",
        
    //     [Country.UNITED_STATES]: "United States",
    //     [Country.CANADA]: "Canada",
    //     [Country.CUBA]: "Cuba",
    //     [Country.MEXICO]: "Mexico",
    // } as Record<string, string>;

    // const mosaServicedStates = {
    //     //Yes
    //     [USState.ARKANSAS]: "Arkansas",
    //     [USState.IOWA]: "Iowa",
    //     [USState.ILLINOIS]: "Illinois",
    //     [USState.INDIANA]: "Indiana",
    //     [USState.KANSAS]: "Kansas",
    //     [USState.KENTUCKY]: "Kentucky",
    //     [USState.MICHIGAN]: "Michigan",
    //     [USState.MINNESOTA]: "Minnesota",
    //     [USState.MISSOURI]: "Missouri",
    //     [USState.NORTH_DAKOTA]: "North Dakota",
    //     [USState.NEBRASKA]: "Nebraska",
    //     [USState.NEW_YORK]: "New York",
    //     [USState.OHIO]: "Ohio",
    //     [USState.PENNSYLVANIA]: "Pennsylvania",
    //     [USState.SOUTH_DAKOTA]: "South Dakota",
    //     [USState.WISCONSIN]: "Wisconsin",

    //     //Maybe
    //     [USState.ALABAMA]: "Alabama",
    //     [USState.COLORADO]: "Colorado",
    //     [USState.GEORGIA]: "Georgia",
    //     [USState.NORTH_CAROLINA]: "North Carolina",
    //     [USState.NEW_JERSEY]: "New Jersey",
    //     [USState.NEW_MEXICO]: "New Mexico",
    //     [USState.TENNESSEE]: "Tennessee",
    //     [USState.TEXAS]: "Texas",

    //     //No
    //     // [USState.ALASKA]: "Alaska",
    //     // [USState.ARIZONA]: "Arizona",
    //     // [USState.CALIFORNIA]: "California",
    //     // [USState.CONNECTICUT]: "Connecticut",
    //     // [USState.DC]: "District Of Columbia",
    //     // [USState.DELAWARE]: "Delaware",
    //     // [USState.FLORIDA]: "Florida",
    //     // [USState.HAWAII]: "Hawaii",
    //     // [USState.IDAHO]: "Idaho",
    //     // [USState.LOUISIANA]: "Louisiana",
    //     // [USState.MASSACHUSETTS]: "Massachusetts",
    //     // [USState.MARYLAND]: "Maryland",
    //     // [USState.MAINE]: "Maine",
    //     // [USState.MISSISSIPPI]: "Mississippi",
    //     // [USState.MONTANA]: "Montana",
    //     // [USState.NEW_HAMPSHIRE]: "New Hampshire",
    //     // [USState.NEVADA]: "Nevada",
    //     // [USState.OKLAHOMA]: "Oklahoma",
    //     // [USState.OREGON]: "Oregon",
    //     // [USState.RHODE_ISLAND]: "Rhode Island",
    //     // [USState.SOUTH_CAROLINA]: "South Carolina",
    //     // [USState.UTAH]: "Utah",
    //     // [USState.VIRGINIA]: "Virginia",
    //     // [USState.VERMONT]: "Vermont",
    //     // [USState.WASHINGTON]: "Washington",
    //     // [USState.WEST_VIRGINIA]: "West Virginia",
    //     // [USState.WYOMING]: "Wyoming",
    // } as Record<string, string>;

    // return {
    //     enumVerbose,
    //     enumAsObject,
    //     mosaServicedStates,
    //     parseDate,
    //     formatDate,
    //     formatCurrency
    // }

    const bob = "bob";
    return {
        bob
    }
}
